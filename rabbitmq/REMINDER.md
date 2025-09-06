# Schulung RabbitMQ – Übersicht & Lernziele

## Kapitel 1: Grundlagen

- **Was ist RabbitMQ?**
  - Einführung: Rolle von RabbitMQ als Message Broker
  - Begriffe: Was ist ein Produzent? Was ist ein Konsument? Was macht RabbitMQ?
- **RabbitMQ Queue = Postfach**
  - Vergleich einer Queue mit einem klassischen Postfach
- **Nachrichtenverteilung**
  - Demonstration: Wie werden Nachrichten an Konsumenten verteilt?
  - Unterschied: Ein Konsument vs. mehrere Konsumenten
- **autoAck-Parameter**
  - Was bewirkt `autoAck=True`?
  - Vor- und Nachteile von automatischer Bestätigung

## Kapitel 2: Zuverlässigkeit und Persistenz

- **Fehlerfall bei autoAck=True**
  - Was passiert, wenn Aufgaben mit `autoAck=True` fehlschlagen?
- **Manuelle Bestätigung**
  - Implementierung: Manuelles Bestätigen einer Nachricht (`delivery_tag = method.delivery_tag`)
  - Wann sollte bestätigt werden?
- **Persistenz von Queues**
  - Unterschied: Nicht-persistente vs. persistente Queues
  - Experiment: RabbitMQ-Server ohne persistente Queue neu starten (mit Nachrichten in der Queue)
- **Persistenz von Nachrichten**
  - Wie werden Nachrichten persistent gespeichert?
  - Voraussetzungen für echte Persistenz (Queue & Message)
- **Message/Task-Verteilung & QoS**
  - Was ist QoS (`basic_qos`)? Warum ist es wichtig?
  - Beispiel: Ein Konsument mit variablem Zeitmultiplikator (mit und ohne QoS)
  - Auswirkungen auf die Lastverteilung und Fairness

---

**Hinweis:**  
Alle Kapitel werden anhand von Python-Beispielen und den offiziellen [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)