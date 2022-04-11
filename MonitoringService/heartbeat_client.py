import sys
from kafka import KafkaProducer
from time import sleep
import time
from datetime import datetime
import threading
import kafka
from requests import get
import json
from flask import Flask, render_template, make_response, jsonify, request, Response

# kafka_ip = '20.219.107.251'
# kafka_port = '9092'

import os
import dotenv
dotenv.load_dotenv()


bootstrap_servers = os.getenv("kafka_bootstrap")


app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/heartbeat', methods=['GET','POST'])
def heartbeat():
    content_type = request.headers.get('Content-Type')
    topic_name = 'logs'
    if (content_type == 'application/json'):
        content = request.json
        
    print(content)
    service_id = content['service_id']
    heart = KafkaProducer(bootstrap_servers=bootstrap_servers,
                          api_version = (0,10,1),
                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print(service_id)
    heart.send(topic_name,{'type' : 'heartbeat','service_id' : service_id,'message' : '1'})

    return Response(content,status=200)



if __name__ == '__main__':

	app.run(debug=False, port="5000", host='0.0.0.0')
