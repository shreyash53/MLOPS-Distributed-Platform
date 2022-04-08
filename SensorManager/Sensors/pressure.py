import sys
from flask import jsonify
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import loads, dumps
import random
from time import sleep
import requests


producer = KafkaProducer(bootstrap_servers=['20.219.107.251:9092'], value_serializer=lambda x:
                         dumps(x).encode('utf-8'))
url = "http://127.0.0.1:8009/"
# while(1):
#     val = requests.post(url).content
#     jsonResponse = json.loads(val.decode('utf-8'))
#         # print("To Topic:")
#         # print(topic_name)
#         # print(jsonResponse)
#     producer.send('S_487548', value=jsonResponse)
#     sleep(5)
while(1):
    try:
        val = requests.post(url).content
        jsonResponse = json.loads(val.decode('utf-8'))
        print(js)
        producer.send('S_17761', value=jsonResponse)
    except:
        pass
    sleep(5)
