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
import numpy as np

app = Flask(__name__)


def get_data():
    return(np.random.choice(np.arange(0, 2), p=[0.95,0.05]))
    # return round(random.uniform(2.0, 5.0), 3)


producer = KafkaProducer(bootstrap_servers=['52.140.63.83:9092'], value_serializer=lambda x:
                         dumps(x).encode('utf-8'))
while(1):

    val = get_data()
    val =val.item()
    # print(type(val))
    print(val)
    producer.send("S_1", value=val)
    sleep(1)

if __name__ == '__main__':
	app.run(debug=True, port=8008, host="0.0.0.0")
