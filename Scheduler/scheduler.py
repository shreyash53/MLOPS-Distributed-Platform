from time import sleep
from flask import Flask, request
import json
from mongoengine.fields import *
import threading
import datetime
from kafka import KafkaProducer

from Utilities.constant import *
from dbconfig import *
from json import dumps


app = Flask(__name__)

db = mongodb()


class Schedules(db.Document):
    app_instance_id = db.StringField(primary=True)
    app_name = db.StringField(required=True)
    app_id = db.StringField(required=True)
    starttime = db.DateTimeField(required=True)
    repetition = db.IntField(required=True)
    interval = db.StringField(required=True)
    endtime = db.DateTimeField(required=True)
    duration = db.DateTimeField(required=False)
    sensors = db.StringField(required=True)


def get_app_instance_id():
    last_id = Schedules.objects.order_by('-app_instance_id').first()
    last_num = int(last_id[4:])
    last_num = last_num+1
    initstr = last_id[:4]+str(last_num)
    return initstr


@app.route('/schedule_application', methods=['POST'])
def scheduleapplication():
    try:
        all_details = request.get_json()
        app_instance_id = get_app_instance_id()
        new_schedule = Schedules(app_instance_id=app_instance_id, app_name=all_details['app_name'], app_id=all_details['app_id'], starttime=parsedatetime(all_details['starttime']), repetition=all_details['repetition'], interval=json.dumps(
            all_details['interval']), endtime=parsedatetime(all_details['endtime']), duration=parsedatetime(all_details['endtime']) - parsedatetime(all_details['starttime']), sensors=json.dumps(all_details['sensors']))

        new_schedule.save()
    except Exception as e:
        return e
    return "OK"


def parsedatetime(date_time_str):
    return datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')


def send_to_deployment_service(type, services):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    for service in services:
        msg = {
            "app_instance_id": service['app_instance_id'],
            "app_name": service['app_name'],
            "request_type": type,
            "app_id": service['app_id'],
            "sensors": service['sensors']
        }
        producer.send(KAFKA_SCHEDULE_TOPIC, json.dumps(msg).encode('utf-8'))
    
    producer.close()


def get_start_services_bw(starttime, endtime):
    res = Schedules.objects('starttime', kwargs={
                            "$lte": endtime, "$gt": starttime}).to_json()
    return res


def get_end_services_bw(starttime, endtime):
    res = Schedules.objects('endtime', kwargs={"$lte": endtime, "$gt": starttime}).to_json()
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

            to_start = get_start_services_bw(slotbegin, slotend)
            to_end = get_end_services_bw(slotbegin, slotend)

            send_to_deployment_service('start',to_start)
            send_to_deployment_service('stop',to_end)
