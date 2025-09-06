#!/usr/bin/env python3
import asyncio
import time
import os
import socket
import sys

from rstream import AMQPMessage, Producer

# Konfiguration aus Umgebungsvariablen
RABBITMQ_HOSTS = os.getenv('RABBITMQ_HOSTS', 'rabbitmq-node1,rabbitmq-node2,rabbitmq-node3').split(',')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
STREAM = "my-test-stream"
MESSAGES = 10
STREAM_RETENTION = 5_000_000_000  # 5 GB

# Versuche eine Verbindung zu einem Host aufzubauen
async def get_connected_producer():
    while True:
        for host in RABBITMQ_HOSTS:
            try:
                socket.gethostbyname(host)
                producer = Producer(
                    host,
                    username=RABBITMQ_USER,
                    password=RABBITMQ_PASS,
                    vhost=RABBITMQ_VHOST
                )
                await producer.__aenter__()
                print(f"[INFO] Verbunden mit RabbitMQ-Host: {host}", file=sys.stderr)
                return producer
            except Exception as e:
                print(f"[WARN] Verbindung zu {host} fehlgeschlagen: {e}", file=sys.stderr)
        print("[INFO] Kein RabbitMQ-Host erreichbar. Neuer Versuch in 5 Sekunden...", file=sys.stderr)
        await asyncio.sleep(5)

# Hauptfunktion zum Senden von Nachrichten
async def publish():
    producer = await get_connected_producer()

    try:
        # Stream erstellen (falls nicht vorhanden)
        await producer.create_stream(
            STREAM,
            exists_ok=True,
            arguments={"MaxLengthBytes": STREAM_RETENTION}
        )

        start_time = time.perf_counter()

        for i in range(MESSAGES):
            amqp_message = AMQPMessage(
                body=f"hello: {i}".encode("utf-8")
            )
            await producer.send(stream=STREAM, message=amqp_message)

        end_time = time.perf_counter()
        print(f"✅ Sent {MESSAGES} messages in {end_time - start_time:0.4f} seconds", file=sys.stderr)

    finally:
        await producer.__aexit__(None, None, None)

# Ausführen
asyncio.run(publish())
