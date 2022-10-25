from threading import Thread
from flask import Flask,request, render_template
import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads
from dbconfig import *
import os
from log_generator import send_log

class applications(db.Document):
    _id = db.StringField(primary_key=True)
    appName = db.StringField(required=True,unique=True)
    path = db.StringField(required=True)
    contract= db.StringField(required=True)

    def to_json(self):
        return {
            "_id": self._id,
            "appName": self.appName,
            "path":self.path,
            "contract":self.contract
        }

class aimodels(db.Document):
    modelName = db.StringField(required=True,unique=True)
    modelId = db.StringField(reqired=True,unique=True)
    #pickleName = db.StringField(required=True)
    path = db.StringField(required=True)
    contract = db.StringField(required=True)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "modelName": self.modelName,
            "modelId":self.modelId,
            #"pickleName":self.pickleName,
            "path":self.path,
            "contract":self.contract
        }

def appdeploy():
    try:    
        consumer = KafkaConsumer(
        'topic_schedule',
        bootstrap_servers=[os.getenv('kafka_bootstrap')],
        auto_offset_reset='earliest', 
        enable_auto_commit=True,
        group_id='group_my',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
        
        producer = KafkaProducer(bootstrap_servers=[os.getenv('kafka_bootstrap')],
                            value_serializer=lambda x: 
                            dumps(x).encode('utf-8'))

        for message in consumer:
            message = message.value
            appName=message.get("app_name")
            # print()
            # print()
            send_log("INFO","Data Recieved:") 
            # print(message)

            app= applications.objects(appName=appName).first()
            # print()
            # print()
            # print(app)
            # print("b n")
            if(app==None):
                continue
            # print("a n")
            # print()
            # print()
            # print()
            # print(app.to_json())
            app=app.to_json()
            loc=app.get('path')
            appId=message.get("app_id")
            contract=app.get('contract')
            contract=json.loads(contract)
            # print()
            # print()
            # print()
            # print(contract)
            appInstanceId=message.get('app_instance_id')
            app_details={}
            app_details["appId"]=appId
            app_details["appName"]=appName
            app_details["appLoc"]=loc
            app_details["appInstanceId"]=appInstanceId
            # print()
            # print()
            # print(app_details)
            models = contract["models"]
            sensors_list=contract["sensors"]
            models_list=[]
            # print()
            # print()
            # print(models)
            # print()
            # print()
            # print(sensors_list)
            for model in models:
                model_details={}
                modelId=model.get("modelid")
                modelname=model.get("modelname")
                # print(modelId)
                # print(modelname)
                model_app= aimodels.objects(modelName=modelname).first()
                if(model_app==None):
                    continue
                model_app=model_app.to_json()
                # print(model_app)
                model_location=model_app.get("path")
                model_details["model_id"]=modelId
                model_details["model_name"]=modelname
                model_details["model_location"]=model_location
                models_list.append(model_details)
            # print("Model list")
            # print(models_list)
            sensors=message.get("sensors")
            sensors=json.loads(sensors)
            data_app={
                "app":app_details,
                "models":models_list,
                "request_type":message.get('request_type'),
                "sensors":sensors
            }
            # print(data_app)
            # producer.send('sensor_list', value=data_sensor)
            # sleep(5)
            send_log("INFO","Data Sent: "+ appId) 

            # print(data_app)
            producer.send('app_deploy2', value=data_app)
            send_log("INFO","Data Sent!!") 
            # print("data sent!!")

    except Exception as e:
        send_log("ERR","Error in scheduler.consumer_thread: "+ e)
        # print('Error in scheduler.consumer_thread', e)
        

def consumer_logic(data):
    model_ = aimodels.objects.filter(modelId = data['service_id'])
    if not model_:
        send_log("INFO",'No model found, now exiting')
        # print('No model found, now exiting')
        return
    model_ = model_.first()
    send_log("INFO",'model found')
    # print('model found')
    request_data = {
        'node' : data['node'],
        'model_id' : data['service_id'],
        'model_location' : model_.path,
        'model_name' : model_.modelName
    }
    producer = KafkaProducer(bootstrap_servers=[os.getenv('kafka_bootstrap')],
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))
    # print('sending data to node manager')
    # print('Request_data: ', request_data)
    producer.send('model_restart', value=request_data)
    
    # sleep(5)
    send_log("INFO",'Restart request sent!!')
    # print("restart request sent!!")

def model_restart_consumer():
    while(1):
        try:    
            consumer = KafkaConsumer(
                'service_dead_model',
                bootstrap_servers=[os.getenv('kafka_bootstrap')],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-group',
                value_deserializer=lambda x: loads(x.decode('utf-8'))
            )
            # print('inside nodemanager consumer thread')
            for data in consumer:
                send_log("INFO",'Model Data Recieved')
                # print(data.value)
                consumer_logic(data.value)

        except Exception as e:
            send_log("ERR","Error in node_manager.consumer_thread"+e)
            # print('Error in node_manager.consumer_thread', e)


class DeploymentConsumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        model_restart_consumer()


if __name__ == '__main__':
    db = mongodb()
    dc = DeploymentConsumer()
    dc.start()
    send_log("INFO","Inside Deployment Service")
    appdeploy()

