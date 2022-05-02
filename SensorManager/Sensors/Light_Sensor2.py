from flask import Flask, request
from time import sleep
from kafka import KafkaConsumer
from flask import Flask
from json import loads
import sys
import numpy as np
app = Flask(__name__)

kafka_server = sys.argv[1]
topic_name = sys.argv[2]

while(1):
    consumer = KafkaConsumer(topic_name,
                             bootstrap_servers=[kafka_server],
                             # auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='my-group',
                             value_deserializer=lambda x: loads(x.decode('utf-8')))
    while(1):
        try:
            for message in consumer:
                message = message.value
                print(message)
                # send_log("INFO","From Topic: {} /n {}".format(topic_name,message))
        except:
            # send_log("ERR", "No Such Controller is active now")
            pass
        sleep(20)
