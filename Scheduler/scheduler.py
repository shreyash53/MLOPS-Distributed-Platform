from time import sleep
from flask import Flask, request
import json
from mongoengine.fields import *
import threading
import datetime
from kafka import KafkaProducer

from Utilities.constant import *
from dbconfig import *
from json import JSONDecodeError


app = Flask(__name__)

db = mongodb()


class Schedules(db.Document):
    _id = db.StringField(primary_key=True)
    app_name = db.StringField(required=True)
    app_id = db.StringField(required=True)
    next_start = db.DateTimeField(required=True)
    next_stop = db.DateTimeField(required=True)
    uptime = db.IntField(required=True)
    downtime = db.IntField(required=True)
    repetition = db.IntField(required=True)
    sensors = db.StringField(required=True)


def get_app_instance_id():
    last_id = Schedules.objects.order_by('-_id').first()

    if last_id is None:
        last_id = "AII_0"
    else:
        last_id = json.loads(last_id.to_json())
        last_id = last_id['_id']

    last_num = int(last_id[4:])
    last_num = last_num+1
    initstr = last_id[:4]+str(last_num)
    return initstr


@app.route('/schedule_application', methods=['POST'])
def scheduleapplication():
    try:
        all_details = request.get_json()
        app_instance_id = get_app_instance_id()
        first_start = parsedatetime(all_details['starttime'])
        first_stop = parsedatetime(all_details['endtime'])
        # TODO: We can reduce some fields here using database reference
        new_schedule = Schedules(_id=app_instance_id,
                                 app_name=all_details['app_name'], 
                                 app_id=all_details['app_id'],
                                 next_start=first_start,
                                 next_stop=first_stop,
                                 uptime= (first_stop - first_start).total_seconds(),
                                 downtime=get_sec_in_json(all_details['interval']),
                                 repetition=all_details['repetition'],
                                 sensors=json.dumps(all_details['sensors']))

        new_schedule.save()
    except Exception as e:
        msg= "err_msg : " + str(e)
        rep ={
            "err_msg":msg
        }
        return rep
    msg= "Scheduled!"
    rep={
        "succ_msg":msg
    }
    return rep


def parsedatetime(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

def get_sec_in_json(j : dict) -> int:
    days = j.get('days', 0)
    hours = j.get('hours', 0)
    minutes = j.get('minutes', 0)
    seconds = j.get('seconds', 0)
    sec = seconds + (60 * (minutes + (60 * (hours + (24 * days)))))
    return sec


def send_to_deployment_service(action, services):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

    if action not in ['start', 'stop']:
        producer.close()
        print("Invalid action :", action)
        return
    if services.count() == 0:
        producer.close()
        print("No services to",action)
        return
    for service in services:
        msg = {
            "app_instance_id": service._id,
            "app_name": service.app_name,
            "request_type": action,
            "app_id": service.app_id,
            "sensors": service.sensors
        }

        old_start = service.next_start
        old_stop = service.next_stop
        uptime = service.uptime
        downtime = service.downtime
        repetition = service.repetition

        if action=="start":
            new_start = old_start + datetime.timedelta(seconds=uptime + downtime)
            repetition -= 1

            service.update(next_start=new_start, repetition=repetition)

        if action=="stop":
            if repetition > 0:
                new_stop = old_stop + datetime.timedelta(seconds=uptime + downtime)
                
                service.update(next_stop=new_stop)
            
            else:
                service.delete()

        producer.send(KAFKA_SCHEDULE_TOPIC, json.dumps(msg).encode('utf-8'))
    
    producer.close()


def get_start_services_bw(starttime, endtime):
    res = Schedules.objects(next_start__lte=endtime, next_start__gt=starttime)
    return res


def get_end_services_bw(starttime, endtime):
    res = Schedules.objects(next_stop__lte=endtime, next_stop__gt=starttime)
    return res


class SchedulingService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            # TODO : A late request from RM can cause events to be missed
            # TODO: We assume that at ANY point, start and stop times are 
            #       ATLEAST further apart than scheduling window. (2min for now)
            now = datetime.datetime.now()
            slotbegin = now - datetime.timedelta(minutes=1)
            slotend = now + datetime.timedelta(minutes=1)

            to_start = get_start_services_bw(slotbegin, slotend)
            to_end = get_end_services_bw(slotbegin, slotend)

            print(f"Scheduling window from {slotbegin} to {slotend}")
            send_to_deployment_service('start', to_start)
            send_to_deployment_service('stop', to_end)

            sleep(30)



if __name__ == "__main__":
    sched = SchedulingService()
    sched.start()
    app.run(host="0.0.0.0", port=8001, debug=False)