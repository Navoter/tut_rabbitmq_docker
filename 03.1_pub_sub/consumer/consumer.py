#!/usr/bin/env python
import pika
import time
import sys
import os
import random
from datetime import datetime

# Umgebungsvariablen für RabbitMQ-Verbindung und Verhalten
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
RABBITMQ_QUEUE_DURABLE = os.getenv('RABBITMQ_QUEUE_DURABLE', 'false').lower() == 'true'
TIME_MULTIPLIER = int(os.getenv('TIME_MULTIPLIER', '1'))

# Steuerung der Verarbeitung und Fehler-Simulation
timeintensive = False       # True: Verarbeitung dauert pro Punkt im Body 1 Sekunde
simulate_error = False      # True: Jeder 2. Nachricht simuliert einen Fehler (keine Ack)
call_count = random.randint(0, 2)  # Startwert für Fehler-Simulation

def callback(ch, method, properties, body):
    """Verarbeitet eingehende Nachrichten."""
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} [x] Received {body.decode()}", file=sys.stderr)
    
    # Simuliere Bearbeitungszeit je nach Anzahl der Punkte im Body
    if timeintensive:
        time.sleep(body.count(b'.') * TIME_MULTIPLIER)
    
    global call_count
    call_count += 1
    # Fehler-Simulation: Jede 2. Nachricht wird nicht bestätigt, Channel wird geschlossen
    if call_count % 2 == 0 and simulate_error:
        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} [!] Message {body.decode()}, No Ack because an ERROR occurred!", file=sys.stderr)
        ch.close()  # Channel schließen, damit RabbitMQ die Nachricht neu verteilt
    else:
        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} [x] Message {body.decode()}, Ack work is Done!", file=sys.stderr)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Nachricht bestätigen

def connect_and_consume():
    """Stellt Verbindung zu RabbitMQ her und startet das Konsumieren der Nachrichten."""
    retries = 5
    while retries > 0:
        try:
            # Jeder Consumer bekommt eine eigene Queue (Hostname als Name)
            amqp_queue = os.uname().nodename
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    virtual_host=RABBITMQ_VHOST,
                    credentials=credentials
                )
            )
            channel = connection.channel()
            # Fanout-Exchange für Publish/Subscribe
            channel.exchange_declare(exchange='logs', exchange_type='fanout')
            # Queue deklarieren (optional: durable für Persistenz)
            channel.queue_declare(queue=amqp_queue, durable=RABBITMQ_QUEUE_DURABLE, exclusive=False)
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} [*] Created a queue '{amqp_queue}' (durable={RABBITMQ_QUEUE_DURABLE})", file=sys.stderr)
            # Queue an Exchange binden
            channel.queue_bind(exchange='logs', queue=amqp_queue)
            # Nachrichten konsumieren
            channel.basic_consume(queue=amqp_queue, on_message_callback=callback)
            print(' [*] Waiting for messages. To exit press CTRL+C', file=sys.stderr)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f" [!] Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            retries -= 1
        except Exception as e:
            print(f" [!] Unerwarteter Fehler: {e}", file=sys.stderr)
            break
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