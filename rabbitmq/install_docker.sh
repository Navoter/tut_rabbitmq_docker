#!/bin/bash

# Das Skript benötigt Root-Rechte, um Docker zu installieren
if [[ $EUID -ne 0 ]]; then
   echo "Dieses Skript muss mit sudo ausgeführt werden."
   exit 1
fi

# Paket-Repository-Informationen aktualisieren
echo "Paketinformationen aktualisieren..."
apt-get update -y

# Notwendige Pakete für das Docker-Repository installieren
echo "Notwendige Pakete installieren..."
apt-get install -y ca-certificates curl gnupg

# Offiziellen GPG-Schlüssel von Docker hinzufügen
echo "Offiziellen Docker GPG-Schlüssel hinzufügen..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Docker-Repository zu den APT-Quellen hinzufügen
echo "Docker-Repository zu den APT-Quellen hinzufügen..."
echo \
  "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  \"$(. /etc/os-release && echo "$VERSION_CODENAME")\" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Paket-Index erneut aktualisieren
echo "Paketindex erneut aktualisieren..."
apt-get update -y

# Docker Engine, CLI und Containerd installieren
echo "Docker Engine, CLI und Containerd installieren..."
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Überprüfen, ob Docker läuft
echo "Docker-Dienststatus überprüfen..."
systemctl status docker --no-pager

echo "Docker wurde erfolgreich installiert."

# Optional: Aktuellen Benutzer zur Docker-Gruppe hinzufügen
# Dies ermöglicht die Ausführung von Docker-Befehlen ohne sudo
# read -p "Möchtest du den aktuellen Benutzer ($USER) zur 'docker' Gruppe hinzufügen, um Docker-Befehle ohne sudo auszuführen? (y/n): " add_user_to_docker_group
# if [[ $add_user_to_docker_group =~ ^[Yy]$ ]]; then
#     echo "Benutzer '$USER' zur 'docker' Gruppe hinzufügen..."
#     usermod -aG docker $USER
#     echo "Du musst dich aus- und wieder einloggen, damit die Gruppenänderung wirksam wird."
# fi

echo "Das Skript ist abgeschlossen."