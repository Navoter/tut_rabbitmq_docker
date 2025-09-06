#!/usr/bin/env python
import pika, time, os, sys

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')

def connect_and_publish(message, severity):
    retries = 5
    while retries > 0:
        try:
            amqp_exchange = 'direct_logs'
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST,
                                        virtual_host=RABBITMQ_VHOST, 
                                        credentials=credentials))
            channel = connection.channel()
            # Cap 03 - Using a 'fanout' exchange
            # channel.exchange_declare(exchange=amqp_exchange, exchange_type='fanout')
            channel.exchange_declare(exchange=amqp_exchange, exchange_type='direct')
            channel.basic_publish(
                exchange=amqp_exchange,
                routing_key=severity,
                body=message)

            print(f" [x] Sent Log '{message}' with '{severity}' to Exchange '{amqp_exchange}'", file=sys.stderr)

            connection.close()
            return
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            retries -= 1
    print("Could not connect to RabbitMQ after multiple retries. Exiting.", file=sys.stderr)

if __name__ == '__main__':
    while True:
        log_messages = [('info', 'This is an info message.'),
                        ('warning', 'This is a warning message.'),
                        ('error', 'This is an error message.'),
                        ('debug', 'This is a debug message.')]
        for severity, log_message in log_messages:
            connect_and_publish(log_message, severity)
        time.sleep(30)