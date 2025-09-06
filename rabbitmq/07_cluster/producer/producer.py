#!/usr/bin/env python
import pika
import time
import os
import logging
import socket # Import the socket module to handle network errors

# Set up logging for clear output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration Section ---
# RABBITMQ_HOSTS can be a comma-separated list of hostnames
RABBITMQ_HOSTS = os.getenv('RABBITMQ_HOSTS', 'rabbitmq-node1,rabbitmq-node2,rabbitmq-node3').split(',')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')

# --- Helper Functions ---
def get_rabbitmq_connection():
    """
    Attempts to establish a connection to any RabbitMQ node in the cluster.
    Handles both RabbitMQ connection errors and network/DNS errors.
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    
    for host in RABBITMQ_HOSTS:
        try:
            logging.info(f"Attempting to connect to RabbitMQ node: {host}")
            parameters = pika.ConnectionParameters(
                host=host,
                virtual_host=RABBITMQ_VHOST,
                credentials=credentials
            )
            connection = pika.BlockingConnection(parameters)
            logging.info(f"Successfully connected to RabbitMQ node: {host}")
            return connection
        except (pika.exceptions.AMQPConnectionError, socket.gaierror) as e:
            logging.warning(f"Failed to connect to {host} due to a network or connection error: {e}")
    
    logging.error("Could not connect to any RabbitMQ node in this cycle.")
    return None

def publish_message(connection):
    """
    Publishes a message to a queue using an existing connection.
    """
    amqp_queue = 'hello'
    message = 'Hello World!'

    try:
        with connection.channel() as channel:
            channel.queue_declare(queue=amqp_queue, 
                                  durable=True, 
                                  arguments={
                                        "x-queue-type": "quorum",
                                        "x-quorum-initial-group-size": 3
                                    })
            channel.basic_publish(exchange='',
                                  routing_key=amqp_queue,
                                  body=message)
            logging.info(f"Sent '{message}' to queue: '{amqp_queue}'")
    except pika.exceptions.AMQPError as e:
        logging.error(f"Failed to publish message: {e}")
        raise # Rethrow the exception to be handled by the main loop
    finally:
        if connection and connection.is_open:
            connection.close()

# --- Main Script Logic ---
if __name__ == '__main__':
    while True:
        try:
            connection = get_rabbitmq_connection()
            if connection:
                publish_message(connection)
                logging.info("Sleeping for 10 seconds before next publish.")
                time.sleep(10)
            else:
                logging.warning("Connection attempt failed. Waiting before next cycle...")
                time.sleep(5)
        except Exception as e:
            logging.error(f"An unexpected error occurred in the main loop: {e}. Retrying after a pause.")
            time.sleep(5)