from flask import Flask,request, render_template
import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads
from dbconfig import *
import os

class applications(db.Document):
    appName = db.StringField(required=True,unique=True)
    path = db.StringField(required=True)
    contract= db.StringField(required=True)

    def to_json(self):
        return {
            "appName": self.appName,
            "path":self.path,
            "contract":self.contract
        }

class aimodels(db.Document):
    modelName = db.StringField(required=True,unique=True)
    path = db.StringField(required=True)
    contract = db.StringField(required=True)
    def to_json(self):
        return {
            "modelName": self.modelName,
            "path":self.path,
            "contract":self.contract
        }

def appdeploy():
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

        print(message)

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
            model_details["model_Id"]=modelId
            model_details["model_name"]=modelname
            model_details["model_location"]=model_location
            models_list.append(model_details)
        # print("Model list")
        # print(models_list)
        sensors=message.get("sensors")
        sensors=json.loads(sensors)
        # print(type(sensors))
        # print(sensors)
        sen_lis=[]
        for each_sensor in sensors_list:
            sen={}
            # print()
            # print("each sensor")
            # print(each_sensor)
            # print(type(sensors))
            # print(sensors)
            for each_bindings in sensors:
                # print("each binding")
                # print(each_bindings)
                if each_sensor['sensorname']==\
                    each_bindings['sensor_name']:
                    sen["sensor_app_id"]=each_sensor['sensorid']
                    sen["sensor_name"]=each_sensor['sensorname']
                    sen["sensor_binding_id"]=each_bindings['sensor_binding_id']
                    sen_lis.append(sen)

        # print()
        # print()
        # print("Final_sensor_list")            
        # print(sen_lis)
        # data_sensor={
        #     "sensor_list":sensors
        # }
        data_app={
            "app":app_details,
            "models":models_list,
            "request_type":message.get('request_type'),
            "sensors":sen_lis
       }
        # print(data_app)
        # producer.send('sensor_list', value=data_sensor)
        # sleep(5)
        print(data_app)
        producer.send('app_deploy1', value=data_app)

        sleep(5)
        print("data sent!!")
    


if __name__ == '__main__':
    db = mongodb()
    appdeploy()

