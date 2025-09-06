#!/usr/bin/env python
import pika, time, os, sys

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')

def connect_and_publish(message, severity, facility):
    retries = 5
    while retries > 0:
        try:
            amqp_exchange = 'topic_logs'
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST,
                                        virtual_host=RABBITMQ_VHOST, 
                                        credentials=credentials))
            channel = connection.channel()
            # Cap 03 - Using a 'fanout' exchange
            # channel.exchange_declare(exchange=amqp_exchange, exchange_type='fanout')
            # Cap 04 - Using a 'direct' exchange
            # channel.exchange_declare(exchange=amqp_exchange, exchange_type='direct')
            channel.exchange_declare(exchange=amqp_exchange, exchange_type='topic')
            channel.basic_publish(
                exchange=amqp_exchange,
                routing_key=severity+'.'+facility, # e.g. "error.auth", "info.cron", "debug.ssh"
                body=message)

            print(f" [x] Sent Log '{message}' with severity: '{severity}' and facility: '{facility}' to Exchange '{amqp_exchange}'", file=sys.stderr)

            connection.close()
            return
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            retries -= 1
    print("Could not connect to RabbitMQ after multiple retries. Exiting.", file=sys.stderr)

if __name__ == '__main__':
    while True:
        log_messages = [('info', 'This is an auth info message.', 'auth'),
                        ('warning', 'This is a cron warning message.', 'cron'),
                        ('error', 'This is a kernel error message.', 'kernel'),
                        ('error', 'This is an auth error message.', 'auth'),
                        ('debug', 'This is a ssh debug message.', 'ssh'),
                        ('info', 'This is a cron info message.', 'cron'),
                        ('warning', 'This is a kernel warning message.', 'kernel'),
                        ('warning', 'This is an auth warning message.', 'auth'),]
        for severity, log_message, facility in log_messages:
            connect_and_publish(log_message, severity, facility)
        time.sleep(30)