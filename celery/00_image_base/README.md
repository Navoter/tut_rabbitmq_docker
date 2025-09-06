Hier ist eine einfache `README.md` im Markdown-Format, die erklärt, wie man aus einem `Dockerfile` ein Docker-Image erstellt.

-----

# Docker Image erstellen

Dieses Repository enthält ein `Dockerfile`, um ein Docker-Image zu bauen.

## 1\. Image bauen

Um das Image zu erstellen, navigieren Sie in das Verzeichnis, das das `Dockerfile` enthält, und führen Sie den folgenden Befehl aus:

```bash
docker build -t [IMAGE_NAME]:[TAG] .
```

  * Ersetzen Sie `[IMAGE_NAME]` durch den gewünschten Namen für Ihr Image (z.B. `meine-app`).
  * Ersetzen Sie `[TAG]` durch eine Versionsnummer oder einen Bezeichner (z.B. `1.0` oder `latest`).
  * Der Punkt `.` am Ende des Befehls gibt den **Build-Kontext** an, d.h., das aktuelle Verzeichnis, in dem sich das `Dockerfile` befindet.

## 2\. Container starten

Nachdem das Image erfolgreich erstellt wurde, können Sie einen Container daraus starten:

```bash
docker run -d -p [HOST_PORT]:[CONTAINER_PORT] --name [CONTAINER_NAME] [IMAGE_NAME]:[TAG]
```

  * `-d`: Startet den Container im **detached mode** (Hintergrundmodus).
  * `-p`: Leitet einen Port vom Host zu einem Port im Container weiter. Ersetzen Sie die Platzhalter entsprechend.
  * `--name`: Gibt dem Container einen eindeutigen Namen.