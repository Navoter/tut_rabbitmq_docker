### Auslastung des RPC-Servers überwachen

Die Berechnung der Fibonacci-Folge ist in diesem Beispiel absichtlich ineffizient implementiert, wodurch die Verarbeitung lange dauert und viele Ressourcen beansprucht. Um die Auslastung des RPC-Servers zu überwachen, kann folgender Befehl verwendet werden:

```bash
docker stats
```

Damit lassen sich CPU- und Speicherauslastung der laufenden Docker-Container in Echtzeit anzeigen.