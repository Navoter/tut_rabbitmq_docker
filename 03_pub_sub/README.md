### Was ist eine Bindung?
Eine Bindung ist die Regel, die RabbitMQ verwendet, um Nachrichten von einem Exchange zu einer Queue zu leiten. Sie ist das Schlüsselelement, das den Fluss von Nachrichten in RabbitMQ steuert. Ohne eine Bindung kann eine Nachricht, die an einen Exchange gesendet wird, keine Queue erreichen

```bash
# Alle Bindes anzeigen lassen
rabbitmqctl list_bindings --vhost=amqp_vhost
```