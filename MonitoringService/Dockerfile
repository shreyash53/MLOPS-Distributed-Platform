FROM python:3.8-slim-buster

RUN mkdir -p /home/app
WORKDIR /home/app


COPY . .
ENV  \   
AZURE_FILESHARE="fileshare" \   
AZURE_STORAGE_NAME="hack2storage" \   
AZURE_STORAGE_KEY="iVYu1uayUo9p0h3k00IdqMpLRX2rSZJ8kldu3cpA3AK6AZqPTuLxd9fmV9zGEmqSqtON0zrlCOTw+AStjdUEGQ==" \   
MONGODB_USER="kamal" \   
MONGODB_PASS="kamal123" \   
MONGODB_CLUSTER="cluster0.lzygp.mongodb.net" \   
REQUEST_MANAGER_PORT=5000 \   
REQUEST_MANAGER_HOST='0.0.0.0' \   
SLCM_PORT=9002 \   
# SCLM_HOST='http://192.168.96.74' \   
SLCM_HOST='http://0.0.0.0' \   
LOG_TOPIC="logs" \   
PORT="9002" \   
kafka_bootstrap='20.219.107.251:9092' \   
service_name="service_name" \   
HOST="0.0.0.0" \   
SCHEDULER_PORT=8001 \   
SCHEDULER_HOST='0.0.0.0' \   
 \   
monitoring_service_name="Monitoring" \   
SLCM_service_name="SLCM" \   
node_manager_service_name="Node_manager" \   
sensor_manager_service_name="Sensor_manager" \   
request_manager_service_name="Request_manager" \   
scheduler_service_name="Scheduler" \   
logging_service_name="Logging" \   
notification_manager_service_name="Notification_manager" \   
deployer_service_name="Deployer" \   
 \   
 \   
monitoring_service_port="5001" \   
SLCM_service_port="9002" \   
node_manager_service_port="6000" \   
sensor_manager_service_port="12000" \   
request_manager_service_port="5000" \   
scheduler_service_port="8001" \   
logging_service_port="15001" \   
notification_manager_service_port="15002" \   
deployer_service_port="15003" \   
 \   
monitoring_service_ip="192.168.21.240" \   
SLCM_service_ip="192.168.21.240" \   
node_manager_service_ip="192.168.21.240" \   
sensor_manager_service_ip="192.168.21.240" \   
request_manager_service_ip="192.168.21.240" \   
scheduler_service_ip="192.168.21.240" \   
logging_service_ip="192.168.21.240" \   
notification_manager_service_ip="192.168.21.240" \   
deployer_service_ip="192.168.21.240"

RUN pip install -r requirements.txt
RUN apt-get update -y && \
    apt-get install curl -y

HEALTHCHECK --interval=20s --timeout=10s  CMD curl --fail -X POST -H "Content-type: application/json" -d "{\"service_id\" : \"John\", \"application_type\" : \"Smith\"}" "http://192.168.21.240:5000/heartbeat" || exit 1


CMD ["python","monitor.py"]