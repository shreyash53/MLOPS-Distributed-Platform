from time import sleep
from flask import Flask,request
import json
from mongoengine.document import Document
from mongoengine.fields import *
import threading
import datetime
from kafka import KafkaConsumer
from kafka import KafkaProducer

from dbconfig import *
from json import dumps


app = Flask(__name__)

db=mongodb()
class Schedules(db.Document):
    app_instance_id = db.StringField(primary = True)
    app_name = db.StringField(required = True)
    app_id = db.StringField(required=True)
    starttime = db.DateTimeField(required=True)
    repetition = db.IntField(required=True)
    interval= db.StringField(required=True)
    endtime = db.DateTimeField(required=True)
    duration = db.DateTimeField(required=False)
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

Scheduling
@app.route('/schedule_application',methods=['POST'])
def scheduleapplication():
    try:
        all_details = request.get_json()
        app_instance_id = get_app_instance_id()
        new_schedule = Schedules(app_instance_id = app_instance_id
                                ,app_name = all_details['app_name']
                                ,app_id = all_details['app_id']
                                ,starttime = parsedatetime(all_details['starttime'])
                                ,repetition = all_details['repetition']
                                ,interval = json.dumps(all_details['interval'])
                                ,endtime = parsedatetime(all_details['endtime'])
                                ,duration = parsedatetime(all_details['endtime']) - parsedatetime(all_details['starttime'])
                                ,sensors = json.dumps(all_details['sensors']))

        new_schedule.save()
    except Exception as e:
        return e
    return "OK"

def parsedatetime(date_time_str):
    return datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

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


def get_services_bw(starttime, endttime):
    res = Schedules.objects(kwargs={"$lte" : endttime, "$gt" : starttime})
    return res

class SchedulingService(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self) 
    
    def run(self):
        while(True):
            sleep(60)
            # TODO : A late request from RM can cause events to be missed
            
            now = datetime.datetime.now()
            slotbegin = now - datetime.timedelta(minutes=1)
            slotend = now + datetime.timedelta(minutes=1)

            to_start = get_services_bw(slotbegin, slotend)


            # send_to_deployment_service('start',appid)
