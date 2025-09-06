## RabbitMQ CLI Cheat Sheet

### Allgemeine Verwaltung (`rabbitmqctl`)
```bash
# Status des Servers anzeigen
rabbitmqctl status

# Liste aller Benutzer
rabbitmqctl list_users

# Benutzer hinzufügen
rabbitmqctl add_user <username> <password>

# Benutzer löschen
rabbitmqctl delete_user <username>

# Benutzerrechte setzen
rabbitmqctl set_permissions -p <vhost> <username> ".*" ".*" ".*"

# Liste aller VHosts
rabbitmqctl list_vhosts

# VHost erstellen
rabbitmqctl add_vhost <vhost>

# VHost löschen
rabbitmqctl delete_vhost <vhost>
```

---

### Zugriff & Rollen
```bash
# Rolle setzen (z. B. administrator)
rabbitmqctl set_user_tags <username> administrator

# Tags anzeigen
rabbitmqctl list_users
```

---

### Queues & Exchanges
```bash
# Liste aller Queues
rabbitmqctl list_queues --vhost amqp_vhost

# Queue löschen
rabbitmqctl delete_queue <queue_name>

# Exchanges anzeigen
rabbitmqctl list_exchanges

# Bindings anzeigen
rabbitmqctl list_bindings
```

---

### Policies & Quorum Queues
```bash
# Quorum Queue Policy setzen
rabbitmqctl set_policy quorum "^celery.*" '{"queue-type":"quorum"}' --apply-to queues

# Policy anzeigen
rabbitmqctl list_policies

# Policy löschen
rabbitmqctl clear_policy <policy_name>
```

---

### Plugins verwalten
```bash
# Plugin aktivieren
rabbitmq-plugins enable rabbitmq_management

# Plugin deaktivieren
rabbitmq-plugins disable <plugin_name>

# Liste aller Plugins
rabbitmq-plugins list
```

---

### Cluster & Nodes
```bash
# Node stoppen
rabbitmqctl stop

# Node neustarten
rabbitmqctl restart

# Cluster beitreten
rabbitmqctl join_cluster rabbit@<node_name>

# Cluster verlassen
rabbitmqctl reset
```

---

### Monitoring & Logs
```bash
# Aktive Verbindungen anzeigen
rabbitmqctl list_connections

# Channels anzeigen
rabbitmqctl list_channels

# Logs anzeigen
tail -f /var/log/rabbitmq/rabbit@<hostname>.log
```