#!/usr/bin/env python
import pika, time, sys, os, random
from datetime import datetime

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
RABBITMQ_QUEUE_DURABLE = os.getenv('RABBITMQ_QUEUE_DURABLE', 'false').lower() == 'true' # Umgebungsvariable für Queue-Durable (true/false)
TIME_MULTIPLIER = int(os.getenv('TIME_MULTIPLIER', '1')) # Umgebungsvariable für Zeitmultiplikator (Standardwert 1)

timeintensive = False   # Setze auf True, um die Verarbeitung zeitintensiv zu machen (1 Sekunden pro Punkt)
simulate_error = False   # Setze auf True, um alle 2. Nachricht einen Fehler zu simulieren
call_count = random.randint(0, 2)  # Zufälliger Startwert, damit nicht immer die Iteration an Nachricht betroffen ist

def callback(ch, method, properties, body):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [x] Received {body.decode()}", file=sys.stderr)
    
    if timeintensive:
        time.sleep(body.count(b'.') * TIME_MULTIPLIER) # Simuliert eine Bearbeitungszeit, indem pro Punkt im Nachrichtentext eine Sekunde gewartet wird
    
    global call_count
    call_count += 1
    if call_count % 2 == 0 and simulate_error:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [!] Message {body.decode()}, No Ack because an ERROR accourse!", file=sys.stderr)
        ch.close()  # Channel schließen, damit RabbitMQ die Nachricht neu verteilt
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  [x] Message {body.decode()}, Ack worke is Done!", file=sys.stderr)
        ch.basic_ack(delivery_tag = method.delivery_tag) # Bestätigung der Nachricht an RabbitMQ senden

def connect_and_consume():
    retries = 5
    while retries > 0:
        try:
            amqp_queue = os.uname().nodename  # Verwende den Hostnamen als Queue-Namen, damit jeder Consumer seine eigene Queue hat
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST,
                                          virtual_host=RABBITMQ_VHOST,
                                          credentials=credentials))
            channel = connection.channel()
            channel.exchange_declare(exchange='logs', exchange_type='fanout')
            # channel.basic_qos(prefetch_count=1) # Stellt sicher, dass ein Konsument nur eine Nachricht gleichzeitig erhält, bis diese bestätigt wurde (ACK).
            channel.queue_declare(queue=amqp_queue, durable=RABBITMQ_QUEUE_DURABLE)
            channel.queue_bind(exchange='logs', queue=amqp_queue)
            channel.basic_consume(queue=amqp_queue, on_message_callback=callback)

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