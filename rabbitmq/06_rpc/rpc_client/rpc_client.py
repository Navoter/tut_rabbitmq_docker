#!/usr/bin/env python
import pika, time, sys, os, uuid
from datetime import datetime
import random

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'rpc_queue')
RETRY_ATTEMPTS = int(os.getenv('RABBITMQ_RETRY_ATTEMPTS', '5'))
RETRY_DELAY = int(os.getenv('RABBITMQ_RETRY_DELAY', '10'))

class FibonacciRpcClient:
    def __init__(self):
        self.credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        self.connection = self._connect_with_retries()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = None

    def _connect_with_retries(self):
        attempts = 0
        while attempts < RETRY_ATTEMPTS:
            try:
                return pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOST,
                        virtual_host=RABBITMQ_VHOST,
                        credentials=self.credentials,
                        heartbeat=60,
                        blocked_connection_timeout=30
                    )
                )
            except pika.exceptions.AMQPConnectionError as e:
                attempts += 1
                print(f"[!] Verbindung zu RabbitMQ fehlgeschlagen: {e}. Versuch {attempts}/{RETRY_ATTEMPTS}", file=sys.stderr)
                if attempts == RETRY_ATTEMPTS:
                    print(f"[!] Konnte nach {RETRY_ATTEMPTS} Versuchen keine Verbindung zu RabbitMQ herstellen.", file=sys.stderr)
                    sys.exit(1)
                time.sleep(RETRY_DELAY)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events(time_limit=1)
        try:
            return int(self.response)
        except Exception:
            return self.response.decode() if isinstance(self.response, bytes) else self.response

if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    while True:
        n = random.randint(10, 40)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [x] Requesting fib({n})", file=sys.stderr)
        response = fibonacci_rpc.call(n)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [.] Got {response}", file=sys.stderr)
        time.sleep(10)