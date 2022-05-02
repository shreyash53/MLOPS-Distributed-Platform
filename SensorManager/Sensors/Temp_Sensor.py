import sys
from flask import Flask, jsonify
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
# from log_generator import send_log
from json import loads, dumps
import random
from time import sleep
import requests

app = Flask(__name__)

def get_data():
    return round(random.uniform(2.0, 5.0), 3)


producer = KafkaProducer(bootstrap_servers=['52.140.63.83:9092'], value_serializer=lambda x:
                         dumps(x).encode('utf-8'))
while(1):
    val = get_data()
    print(val)
    producer.send("S_1", value=val)
    sleep(20)

if __name__ == '__main__':
	app.run(debug=True, port=8008, host="0.0.0.0")
