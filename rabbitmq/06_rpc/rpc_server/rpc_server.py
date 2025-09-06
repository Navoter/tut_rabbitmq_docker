#!/usr/bin/env python
import pika, time, os, sys
from datetime import datetime

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'rpc_queue')
RETRY_ATTEMPTS = int(os.getenv('RABBITMQ_RETRY_ATTEMPTS', '5'))
RETRY_DELAY = int(os.getenv('RABBITMQ_RETRY_DELAY', '10'))

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    try:
        n = int(body)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  [.] fib({n})", file=sys.stderr)
        response = fib(n)
    except Exception as e:
        print(f" [!] Fehler bei der Verarbeitung: {e}", file=sys.stderr)
        response = "error"
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def connect_and_serve():
    retries = RETRY_ATTEMPTS
    while retries > 0:
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    virtual_host=RABBITMQ_VHOST,
                    credentials=credentials,
                    heartbeat=60,
                    blocked_connection_timeout=30
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=on_request)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  [x] Awaiting RPC requests", file=sys.stderr)
            channel.start_consuming()
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f" [!] Verbindung zu RabbitMQ fehlgeschlagen: {e}. Neuer Versuch in {RETRY_DELAY} Sekunden...", file=sys.stderr)
            time.sleep(RETRY_DELAY)
            retries -= 1
        except Exception as e:
            print(f" [!] Unerwarteter Fehler: {e}", file=sys.stderr)
            break
    else:
        print(" [!] Konnte nach mehreren Versuchen keine Verbindung zu RabbitMQ herstellen. Beende.", file=sys.stderr)

if __name__ == '__main__':
    try:
        connect_and_serve()
    except KeyboardInterrupt:
        print(' [x] Beendet durch Benutzer', file=sys.stderr)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

