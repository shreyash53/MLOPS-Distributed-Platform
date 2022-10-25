#!/bin/bash
sudo apt-get update
sudo apt-get -y install python3.8-venv
sudo apt-get -y install docker
sudo apt-get -y install docker-compose
sudo apt-get -y install python3.8-venv
sudo apt-get -y install azure-cli
sudo apt-get -y install rsync
sudo apt-get -y install openssh-client

sudo mkdir -p /lib/docker/cli-plugins
cd /lib/docker/cli-plugins
sudo wget -q https://github.com/docker/buildx/releases/download/v0.8.2/buildx-v0.8.2.linux-amd64
sudo mv buildx-v0.8.2.linux-amd64 docker-buildx
sudo chmod +x docker-buildx

sudo usermod -aG docker azureuser
sudo timedatectl set-timezone Asia/Kolkata

cd ~/ChildNode/
python3 -m venv shra
source ./shra/bin/activate
pip install -r requirements.txt
python child_node_bootstrap.py $1 $2
# python bootstrap.py
deactivate