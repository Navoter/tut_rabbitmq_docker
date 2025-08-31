#!/usr/bin/env python
import pika, time, os, sys

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
RABBITMQ_QUEUE_DURABLE = os.getenv('RABBITMQ_QUEUE_DURABLE', 'false').lower() == 'true' # Umgebungsvariable für Queue-Durable (true/false)
RABBITMQ_DELIVERY_MODE = int(os.getenv('RABBITMQ_DELIVERY_MODE', '1')) # Umgebungsvariable für delivery_mode (1=non-persistent, 2=persistent)

def connect_and_publish(message):
    retries = 5
    while retries > 0:
        try:
            amqp_queue = 'hello'
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST,
                                        virtual_host=RABBITMQ_VHOST, 
                                        credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue=amqp_queue, durable=RABBITMQ_QUEUE_DURABLE)

            channel.basic_publish(
                exchange='',
                routing_key=amqp_queue,
                body=message,
                properties=pika.BasicProperties(delivery_mode=RABBITMQ_DELIVERY_MODE)
            )
            print(f" [x] Sent '{message}' (delivery_mode={RABBITMQ_DELIVERY_MODE})", file=sys.stderr)

            connection.close()
            return
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            retries -= 1
    print("Could not connect to RabbitMQ after multiple retries. Exiting.", file=sys.stderr)

if __name__ == '__main__':
    while True:
        messages = ['First.', 'Second..', 'Third...', 'Fourth....', 'Fifth.....']
        for message in messages:
            connect_and_publish(message)
        time.sleep(30)