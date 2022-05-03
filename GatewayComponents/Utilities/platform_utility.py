import os
import requests
from kafka import KafkaConsumer, KafkaProducer
from filecmp import dircmp
from PIL import Image
from io import BytesIO
import numpy as np
import json
import cv2
from json import dumps
import dotenv
dotenv.load_dotenv()


ns = os.getenv("num_sensors") # number of sensors
nm = os.getenv("num_models") # number of models

url = os.getenv('url')
PORT = os.getenv("SERVICE_PORT")

sensors = dict()
sensor_ids_list = '<sensor_ids>'

for s_id in sensor_ids_list:
	sname = "S_"+str(s_id)
	sensors[sname] = os.getenv(sname) 

for s_id in sensor_ids_list:
	sname = "S_"+str(s_id)
	sensors[sname] = os.getenv(sname) 

# KAFKA_IP = "52.140.63.83:9092"
KAFKA_IP = os.getenv('kafkaurl')

def  getsensordata(sensor_id):
	sensor_id = "S_" + str(sensor_id)
	url_ = url + '/api' + '/sensor' + '/'+ sensor_id ##sensors[sensor_id]
	response = requests.get(url_)
	# if response.status_code ==200:
	res = response.json()
	return res['data']


def getmodeldata(model_id,data,route):
    # url_ = url + "/model/" + model_id
    url_ = url + '/api' + '/model' + '/' + model_id + "?route=" + route
    response = requests.post(url_ , json = data)
    res = response.json()
    return res['result']


def getsensordata1(sensor_id):
    sensor_topic = "S_" + sensors[sensor_id]
    # sensor_topic = sensors[sensor_id]
    print("Sensor_Tpic: ", sensor_topic)
    res = getkafkadata(sensor_topic)
    
    return res['data']


def getkafkadata(topic):
    consumer = KafkaConsumer(topic,bootstrap_servers=[KAFKA_IP], max_partition_fetch_bytes=19048576)
    for message in consumer:
        print("Message Recieved: ", topic)
        try:
            res = json.loads(message.value)
            data = {
                'data':res
            }
            return data
        except:
            stream = BytesIO(message.value)
        # print("Stream:", type(stream.getvalue()))
        image = Image.open(stream).convert("RGB")
        frame = np.array(image)
        stream.close()
        # image.show()
        image = frame.tolist()
        data = {
            'data': {
                'image': image
            }
        }

        return data

def setkafkadata(sensor_topic,val):
    producer = KafkaProducer(bootstrap_servers=[KAFKA_IP],value_serializer=lambda x: dumps(x).encode('utf-8'))
    producer.send(sensor_topic, value=val)


def setcontrollerdata(sensor_id,val):
    sensor_topic = "S_" + sensors[sensor_id]
    # sensor_topic = sensors[sensor_id]
    print("Sensor_Tpic: ", sensor_topic)
    setkafkadata(sensor_topic,val)