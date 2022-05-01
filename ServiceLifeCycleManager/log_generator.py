import os
from dotenv import load_dotenv
import json
from kafka import KafkaProducer

load_dotenv()

log_topic = os.getenv("KAFKA_LOG_TOPIC")
kafka_server = os.getenv("kafka_bootstrap")
SERVICE_NAME = os.getenv("SLCM_service_name") #<= change here
print(log_topic)
# TODO: change service name env variable 
# logs = KafkaProducer(bootstrap_servers=kafka_server,value_serializer=lambda x:dumps(x).encode('utf-8'))
print(kafka_server)

def send_log(log_type, msg ):
    print("hit")
    logs = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda x:json.dumps(x).encode('utf-8'))
    possible_log_type = ['INFO', 'WARN', 'ERR']
    if log_type not in possible_log_type:
        raise Exception('ERR: log_type provided is wrong\n It should be INFO, WARN or ERR')
    print("sasdsadsadasds")
    data = {"type" : log_type , "service_name" : SERVICE_NAME,"msg" : msg}
    logs.send(log_topic, data)
    return 1

		

