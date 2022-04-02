from flask import Flask,request, render_template
import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads
from dbconfig import *

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
    'scheduler12',
     bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', 
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))
    
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))

    for message in consumer:
        message = message.value
        appName=message.get("app_name")
        print('{} added to {}'.format(appName, message))
        app= applications.objects(appName=appName).first()
        print()
        print(app.to_json())
        app=app.to_json()
        loc=app.get('path')
        appId=app.get('_id')
        contract=app.get('contract')
        print(contract)
        contract=json.loads(contract)
        print()
        print(contract)
        appInstanceId=message.get('app_instance_id')
        app_details={}
        app_details["appId"]=appId
        app_details["appName"]=appName
        app_details["appLoc"]=loc
        app_details["appInstanceId"]=appInstanceId
        print(app_details)
        models = contract["models"]
        models_list=[]
        print()
        print(models)
        for model in models:
            model_details={}
            modelId=model.get("modelid")
            modelname=model.get("modelname")
            print(modelId)
            print(modelname)
            model_app= aimodels.objects(modelName=modelname).first()
            model_app=model_app.to_json()
            print(model_app)
            model_location=model_app.get("path")
            model_details["model_Id"]=modelId
            model_details["model_name"]=modelname
            model_details["model_location"]=model_location
            models_list.append(model_details)
        print(models_list)
        sensors=message.get("sensors")
        print(sensors)
        data_sensor={
            "sensor_list":sensors
        }
        data_app={
            "app":app_details,
            "models":models_list,
            "request_type":message.get('request_type')
       }
        producer.send('sensor_list', value=data_sensor)
        sleep(5)
        producer.send('app_deploy', value=data_app)
        sleep(5)
    


if __name__ == '__main__':
    db = mongodb()
    appdeploy()

    