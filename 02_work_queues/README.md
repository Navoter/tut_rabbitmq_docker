## README: RabbitMQ Docker-Compose Projekt

### Tutorial:
https://www.rabbitmq.com/tutorials/tutorial-two-python

### Projektübersicht

Dieses Projekt demonstriert die grundlegende Nutzung von RabbitMQ in einem Docker-Compose-Setup. Es besteht aus drei Services: einem **RabbitMQ-Server**, einem **Python Producer** und einem **Python Consumer**. Der Producer sendet eine Nachricht an den RabbitMQ-Server, während der Consumer diese Nachricht empfängt und verarbeitet.

### Voraussetzungen

Stellen Sie sicher, dass **Docker** und **Docker Compose** auf Ihrem System installiert sind.

-----

### Schnelleinstieg

1.  **Repository klonen**:
    ```bash
    git clone https://github.com/your-username/your-project.git
    cd your-project
    ```
2.  **Umgebungsvariablen festlegen**: Erstellen Sie eine `.env`-Datei im Hauptverzeichnis und fügen Sie Ihre RabbitMQ-Zugangsdaten und den VHost hinzu:
    ```ini
    RABBITMQ_DEFAULT_USER=myuser
    RABBITMQ_DEFAULT_PASS=mypassword
    RABBITMQ_VHOST=my_app_vhost
    ```
3.  **Container starten**: Verwenden Sie Docker Compose, um alle Services im Hintergrund zu starten.
    ```bash
    docker compose up -d
    ```
4.  **Logs prüfen**: Überprüfen Sie die Container-Logs, um die Ausgabe des Producers und Consumers zu sehen.
    ```bash
    docker compose logs -f
    ```
    Der Producer sendet eine Nachricht ("Hello World\!") und beendet sich, während der Consumer die Nachricht empfängt und dann auf weitere Nachrichten wartet.

-----

### Projektstruktur

Die Verzeichnisstruktur des Projekts sieht wie folgt aus:

```
.
├── docker-compose.yml
├── .env
├── Justfile
├── producer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── producer.py
└── consumer/
    ├── Dockerfile
    ├── requirements.txt
    └── consumer.py
```

  - **`docker-compose.yml`**: Definiert die drei Docker-Services (`rabbitmq`, `producer`, `consumer`).
  - **`.env`**: Speichert Umgebungsvariablen wie Benutzernamen und Passwörter.
  - **`Justfile`**: Bietet einfache, wiederverwendbare Befehle für die Docker-Verwaltung.
  - **`producer/` & `consumer/`**: Enthalten jeweils das `Dockerfile` und das Python-Skript für den Producer bzw. Consumer.

-----

### Docker-Services

  - **`rabbitmq`**:
      - Verwendet das offizielle `rabbitmq:3.13-management` Image, das eine Admin-Oberfläche unter `http://localhost:15672` zur Verfügung stellt (Login mit den `.env`-Daten).
      - Die Benutzerdaten werden über Umgebungsvariablen konfiguriert, die aus der `.env`-Datei geladen werden.
  - **`producer` & `consumer`**:
      - Beide Services werden aus ihren jeweiligen Verzeichnissen (`./producer` und `./consumer`) gebaut.
      - Sie verwenden ein schlankes **Alpine Linux**-Image als Basis, um die Image-Größe zu minimieren.
      - Die Python-Skripte (`producer.py` und `consumer.py`) werden als Volume gemountet, was eine schnelle Entwicklung ermöglicht, ohne die Images neu bauen zu müssen.
      - Sie verbinden sich mit RabbitMQ unter Verwendung der in der `.env` definierten Zugangsdaten und des VHosts.

-----

### Nützliche Befehle

Verwenden Sie `just` für die einfache Ausführung von Befehlen.

| Befehl | Beschreibung |
| :--- | :--- |
| `just up` | Startet alle Container im Hintergrund. |
| `just up-logs` | Startet alle Container im Vordergrund (zum Debuggen). |
| `just down` | Stoppt und entfernt alle Container, Netzwerke und Volumes. |
| `just rebuild` | Baut die Producer- und Consumer-Images neu und startet die Container. |
| `just restart-producer` | Startet nur den Producer-Container neu. |
| `just logs` | Zeigt die Echtzeit-Logs aller Container. |

Wenn Sie `just` nicht verwenden, können Sie die entsprechenden `docker compose`-Befehle direkt ausführen (z.B. `docker compose up -d`).

-----

### Anpassung

  - **RabbitMQ-Zugangsdaten**: Passen Sie die Werte in der `.env`-Datei an, um Ihre eigenen Zugangsdaten zu verwenden.
  - **Python-Skripte**: Ändern Sie die Logik in `producer.py` und `consumer.py`, um komplexere Nachrichten-Workflows zu implementieren.
  - **`requirements.txt`**: Fügen Sie weitere Python-Bibliotheken hinzu, die Ihr Projekt benötigt.


```bash
# Anzeigen der anzahl nicht bestätigter Messages
rabbitmqctl list_queues name messages_ready messages_unacknowledged --vhost=amqp_vhost

# Alle Comsumer container neu starten
docker compose restart consumer

# Logs von allen Consumer containern anzeigen
docker compose logs consumer -f

# Container neu erstellen lassen
docker compose up --force-recreate consumer
```