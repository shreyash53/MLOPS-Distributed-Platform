import sys
from flask import jsonify
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import loads,dumps
import random
from time import sleep
import requests

# topic_name=sys.argv[1]
# is_sensor = sys.argv[2]
# ip = sys.argv[3]
# port = sys.argv[4]


# def get_data():
#     randomlist = random.sample(range(1, 10000000), 10)
#     return randomlist

def fun(topic_name,ip,port,time):
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
        url = "http://"+str(ip)+":"+str(port)+"/"
        while(1):
            val = requests.post(url).content
            jsonResponse = json.loads(val.decode('utf-8'))
            # print("To Topic:")
            # print(topic_name)
            # print(jsonResponse)
            producer.send(topic_name, value=jsonResponse)
            sleep(time)

def fun2(topic_name, ip, port,time):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        # auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    while(1):
        for message in consumer:
            # print("From Topic:")
            # print(topic_name)
            message=message.value
            url = "http://"+str(ip)+":"+str(port)+"/"
            requests.post(url, json=message)
            sleep(time)

# if(is_sensor):
#     fun(topic_name, ip, port)
# else:
#     fun2(topic_name, ip, port)





