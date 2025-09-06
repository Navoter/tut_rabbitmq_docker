#!/usr/bin/env python3
import asyncio
import signal
import os
import sys
import socket

from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    amqp_decoder,
    OnClosedErrorInfo,
)

# Konfiguration
RABBITMQ_HOSTS = os.getenv('RABBITMQ_HOSTS', 'rabbitmq-node1,rabbitmq-node2,rabbitmq-node3').split(',')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'mypassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'myvhost')
STREAM = "my-test-stream"
PORT = 5552

# Globale Variablen
active_consumer = None
reconnect_event = asyncio.Event()


async def on_connection_closed(disconnection_info: OnClosedErrorInfo) -> None:
    print(
        "[WARN] Verbindung wurde geschlossen von Stream(s): "
        + str(disconnection_info.streams)
        + " Grund: "
        + str(disconnection_info.reason),
        file=sys.stderr
    )
    reconnect_event.set()


async def on_message(msg: AMQPMessage, message_context: MessageContext):
    stream = message_context.consumer.get_stream(message_context.subscriber_name)
    offset = message_context.offset
    print(f"📥 Got message: {msg.body.decode()} from stream {stream}, offset {offset}", file=sys.stderr)


async def run_consumer(host):
    global active_consumer
    reconnect_event.clear()

    consumer = Consumer(
        host=host,
        port=PORT,
        vhost=RABBITMQ_VHOST,
        username=RABBITMQ_USER,
        password=RABBITMQ_PASS,
        on_close_handler=on_connection_closed
    )

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(consumer.close()))

    try:
        await consumer.create_stream(STREAM, exists_ok=True)
    except Exception:
        pass  # Stream existiert vermutlich schon

    await consumer.start()
    await consumer.subscribe(stream=STREAM, callback=on_message, decoder=amqp_decoder)
    active_consumer = consumer

    # Warte bis Verbindung geschlossen wird
    await reconnect_event.wait()

    # Verbindung wurde geschlossen → sauber schließen
    try:
        await consumer.close()
    except Exception:
        pass
    active_consumer = None


async def main():
    while True:
        for host in RABBITMQ_HOSTS:
            try:
                socket.gethostbyname(host)
                print(f"[INFO] Versuche Verbindung zu {host}...", file=sys.stderr)
                await run_consumer(host)
                break  # Wenn erfolgreich, verlasse Host-Schleife
            except Exception as e:
                print(f"[WARN] Verbindung zu {host} fehlgeschlagen: {e}", file=sys.stderr)

        print("[INFO] Neuer Versuch in 5 Sekunden...", file=sys.stderr)
        await asyncio.sleep(5)


asyncio.run(main())
