#!/usr/bin/env python
import pika, time, sys, os
from datetime import datetime

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
TIME_MULTIPLIER = int(os.getenv('TIME_MULTIPLIER', '1')) # Umgebungsvariable für Zeitmultiplikator (Standardwert 1)

timeintensive = False   # Setze auf True, um die Verarbeitung zeitintensiv zu machen (1 Sekunden pro Punkt)

def callback(ch, method, properties, body):
    if timeintensive:
        time.sleep(body.count(b'.') * TIME_MULTIPLIER) # Simuliert eine Bearbeitungszeit, indem pro Punkt im Nachrichtentext eine Sekunde gewartet wird
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [x] Received {body.decode()}", file=sys.stderr)

def connect_and_consume():
    retries = 5
    while retries > 0:
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST,
                                          virtual_host=RABBITMQ_VHOST,
                                          credentials=credentials))
            channel = connection.channel()
            channel.exchange_declare(exchange='logs', exchange_type='fanout')
            result = channel.queue_declare(queue='', exclusive=True)
            amqp_queue = result.method.queue
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [*] Created an exclusive temporary queue '{amqp_queue}'", file=sys.stderr)
            channel.queue_bind(exchange='logs', queue=amqp_queue)
            channel.basic_consume(queue=amqp_queue,
                                  on_message_callback=callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C', file=sys.stderr)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f" [!] Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            retries -= 1
    print(" [!] Could not connect to RabbitMQ after multiple retries. Exiting.", file=sys.stderr)

def main():
    connect_and_consume()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)