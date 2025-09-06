#!/usr/bin/env python
import pika, time, os, sys

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')

def connect_and_publish():
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
            channel.queue_declare(queue=amqp_queue)

            message = 'Hello World!'
            channel.basic_publish(exchange='',
                                  routing_key=amqp_queue,
                                  body=message)
            print(f" [x] Sent '{message}' to Queue: '{amqp_queue}' ", file=sys.stderr)

            connection.close()
            return
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            retries -= 1
    print("Could not connect to RabbitMQ after multiple retries. Exiting.", file=sys.stderr)

if __name__ == '__main__':
    while True:
        connect_and_publish()
        time.sleep(10)