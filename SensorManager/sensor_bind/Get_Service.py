import sys
from flask import jsonify
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from log_generator import send_log
from json import loads,dumps
import random
from time import sleep
import requests

import os
import dotenv
dotenv.load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("kafka_bootstrap")

# topic_name=sys.argv[1]
# is_sensor = sys.argv[2]
# ip = sys.argv[3]
# port = sys.argv[4]


# def get_data():
#     randomlist = random.sample(range(1, 10000000), 10)
#     return randomlist

def fun(topic_name,ip,port,time):
        producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS], value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
        url = "http://"+str(ip)+":"+str(port)+"/"
        while(1):
            try:
                val = requests.post(url).content
                jsonResponse = json.loads(val.decode('utf-8'))
                dic = {}
                dic['data'] = jsonResponse
                producer.send(topic_name, value=dic)
                # send_log("INFO","To Topic: {} /n {}".format(topic_name,dic))
                # print("To Topic:")
                # print(topic_name)
                # print(dic)
            except:
                send_log("ERR" ,"No Sensor is active right now")
                pass
            sleep(time)

def fun2(topic_name, ip, port,time):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[BOOTSTRAP_SERVERS],
        # auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    while(1):
        try:
            for message in consumer:
                # print("From Topic:")
                # print(topic_name)
                message=message.value
                # send_log("INFO","From Topic: {} /n {}".format(topic_name,message))
                url = "http://"+str(ip)+":"+str(port)+"/"
                requests.post(url, json=message)
        except:
            send_log("ERR" ,"No Such Controller is active now")
            pass
        sleep(time)

# if(is_sensor):
#     fun(topic_name, ip, port)
# else:
#     fun2(topic_name, ip, port)





