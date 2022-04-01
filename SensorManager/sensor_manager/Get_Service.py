import sys
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import loads,dumps
import random
from time import sleep
import requests


topic_name= sys.argv[1]
is_sensor=sys.argv[2]
ip=sys.argv[3]
port=sys.argv[4]


def get_data():
    randomlist = random.sample(range(1, 10000000), 10)
    return randomlist

if(is_sensor):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    url = "http://"+str(ip)+":"+str(port)+"/"
    while(1):
        val =requests.post(url).content
        jsonResponse = json.loads(val.decode('utf-8'))
        print(jsonResponse)
        producer.send(topic_name, value=jsonResponse)
        sleep(1)

    # for e in range(1000):
    #     data = {'number': e}
    #     producer.send(topic_name, value=data)
    #     sleep(5)
else:
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        print(message)
        sleep(0.2)


