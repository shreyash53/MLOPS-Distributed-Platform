from kafka import KafkaProducer
from json import dumps
from time import sleep
producer = KafkaProducer(bootstrap_servers='localhost:9093',value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
data = {
    'type':'not_heartbeat',
    'service_name':'node_Manager',
    'msg':'this is msg',
    'time':'00:00'
}
topic_name = 'logs'
temp = 10
while temp>0:
    temp = temp - 1
    producer.send(topic_name,data)
    print("sent")
    sleep(1)