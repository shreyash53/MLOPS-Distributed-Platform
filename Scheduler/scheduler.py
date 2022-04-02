from operator import eq
from flask import Flask,request
from json import loads
import json
from mongoengine.document import Document
from mongoengine.fields import *
import pymongo
import threading
import datetime
from kafka import KafkaConsumer
from kafka import KafkaProducer

from ias_hacka2.dbconfig import mongodb
from ias_hacka2.scheduler import get_cur_date_time


from Utilities.constants import *
from json import dumps


app = Flask(__name__)

db=mongodb()
class Schedules(db.Document):
    app_instance_id = db.StringField(primary = True)
    app_name = db.StringField(required = True)
    app_id = db.StringField(required=True)
    starttime = db.StringField(required=True)
    repetition = db.IntField(required=True)
    interval= db.StringField(required=True)
    endtime = db.StringField(required=True)
    sensors = db.StringField(required=True)

    def to_json(self):
        return {
            "app_instance_id":self.app_instance_id,
            "app_name":self.app_name,
            "app_id":self.app_id,
            "starttime":self.starttime,
            "repetition":self.repetition,
            "interval":self.interval,
            "endtime":self.endtime,
            "sensors":self.sensors
        }

def get_app_instance_id():
    last_id = Schedules.objects.order_by('-app_instance_id').first()
    last_num = int(last_id[4:])
    last_num=last_num+1
    initstr=last_id[:4]+str(last_num)
    return initstr


@app.route('/schedule_application',methods=['POST'])
def scheduleapplication():
    try:
        all_details = request.get_json()
        app_instance_id = get_app_instance_id()
        new_schedule = Schedules(app_instance_id = app_instance_id
                                ,app_name = all_details['app_name']
                                ,app_id = all_details['app_id']
                                ,starttime = all_details['starttime']
                                ,repetition = all_details['repetition']
                                ,interval = json.dumps(all_details['interval'])
                                ,endtime = all_details['endtime']
                                ,sensors = json.dumps(all_details['sensors']))

        new_schedule.save()
    except Exception as e:
        return e
    return "OK"

def get_cur_Time():
    cur_datetime = datetime.datetime.now()
    IST_date_time = cur_datetime + datetime.timedelta(minutes = 330)
    IST_date_time = str(IST_date_time)
    date, time = IST_date_time.split(' ')
    cur_time = (time.split('.'))[0]
    hour, minute, second = cur_time.split(':')
    return date, hour, minute


# def getKafka_credentials():
#     f = open('filename', "r")
#     data = json.loads(f.read())
#     ip = data['ip']
#     port = str(data['port'])
#     return ip,port


def send_to_deployment_service(type1, message):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    message = type1 + message
    producer.send('deployer_service', json.dumps(message).encode('utf-8'))
    producer.flush()
    producer.close()


class StartService(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self) 
    
    def run(self):
        while(True):
            today,HH,MM=get_cur_Time()
            hour = int(HH)
            minute=int(MM)
            mycursor=db.Scheduling.find({ 'startdate':today })

            # send_to_deployment_service('start',appid)


class EndService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass
