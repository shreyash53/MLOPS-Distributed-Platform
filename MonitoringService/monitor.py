from pydoc_data import topics
import sys
from flask import request
import kafka
from dbconfig import *
from kafka import KafkaProducer
from kafka import KafkaConsumer
from time import sleep
import time
from datetime import datetime
import threading
from requests import get,post
import json
import os
import mongoengine as db
import dotenv
from flask import Flask, render_template, make_response, jsonify, request, Response



dotenv.load_dotenv()

# db = mongodb()

PORT_SLCM = os.getenv("SLCMIP")

kafka_ip = '127.0.0.1'
kafka_port = '9092'


def deregister(message):
    global registered_services
    print("deregister",message)
    data = {
        "instance_id" : message
    }
    print(data)
    post('http://{}/service_dead'.format(PORT_SLCM),json=data)
    # dereg = RegisteredServices.objects(service_id = message)
    # dereg.delete()
    del registered_services[message]

def log_reader():
    topic_name='logs'

    global registered_services
    consumer = KafkaConsumer(topic_name,bootstrap_servers='{}:{}'.format(kafka_ip,kafka_port),api_version = (0,10,1),)
    for message in consumer:

        msg=json.loads(message.value.decode('utf-8'))
        print(msg)
        if msg['type']=='flush':
            for k in list(registered_services.keys()):
                if time.time()-registered_services[k]>=30:
                    print("{} stopped working".format(k))
                    deregister(k)
                    continue
                # newregistered = RegisteredServices(service_id=k,timestamp=registered_services[k])
                # newregistered.save()
        if msg['type']=='heartbeat':
            if msg['service_id'] not in registered_services.keys():
                print("new service started")
                registered_services[msg['service_id']] = time.time()
            else:
                registered_services[msg['service_id']] = time.time()
            
            continue

def register(message):
    registered_services[message['service_id']] = time.time()
    print(registered_services)

def flush():
    flush = KafkaProducer(bootstrap_servers='{}:{}'.format(kafka_ip,kafka_port),
                          api_version = (0,10,1),
                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    while True:
        flush.send('logs',{'type' : 'flush','service_id' : 0,'message' : '1'})
        time.sleep(10)

registered_services = {}

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/heartbeat', methods=['GET','POST'])
def heartbeat():
    try:
        content_type = request.headers.get('Content-Type')
        topic_name = 'logs'
        if (content_type == 'application/json'):
            content = request.json

        service_id = content['instance_id']
        heart = KafkaProducer(bootstrap_servers='{}:{}'.format(kafka_ip,kafka_port),
                              api_version = (0,10,1),
                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        print(service_id)
        heart.send(topic_name,{'type' : 'heartbeat','service_id' : service_id,'message' : '1'})
    except Exception as e:
        return Response(e,status=400)

    return Response(content,status=200)

def runflask():
    app.run(host='localhost',port=5000,debug=False)


if __name__ == "__main__":

    # for x in RegisteredServices.objects:
        # registered_services[x['service_id']] = x['timestamp']
    
    threading.Thread(target=flush).start()
    threading.Thread(target=log_reader()).start()
    runflask()


