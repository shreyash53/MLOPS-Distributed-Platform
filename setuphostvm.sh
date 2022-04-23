#!/bin/bash

apt update
apt --yes --force-yes install docker
apt --yes --force-yes install docker-compose
apt --yes --force-yes install python3.8-venv
apt --yes --force-yes install azure-cli


mkdir -p /lib/docker/cli-plugins
cd /lib/docker/cli-plugins
wget https://github.com/docker/buildx/releases/download/v0.8.2/buildx-v0.8.2.linux-amd64
mv buildx-v0.8.2.linux-amd64 docker-buildx
chmod +x docker-buildx

usermod -aG docker azureuser
timedatectl set-timezone Asia/Kolkata
reboot

echo "Restart your VM now....."