import sys
from flask import jsonify
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import loads,dumps
import random
from time import sleep
import requests
consumer = KafkaConsumer(
    'S2_487548',
    bootstrap_servers=['20.219.107.251:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
while(1):
    for message in consumer:
        # print("From Topic:")
        # print(topic_name)
        message = message.value
        print(message)
        # url = "http://"+str(ip)+":"+str(port)+"/"
        # requests.post(url, json=message)
        # sleep(5)
