from time import sleep
from flask import Flask, request
import json
from mongoengine.fields import *
import threading
import datetime
from kafka import KafkaProducer, KafkaConsumer
from json import loads

from log_generator import send_log
from utilities.constant import *
from dbconfig import *
import time

import os
import dotenv
dotenv.load_dotenv()

HOST = os.getenv('SCHEDULER_HOST')
PORT = os.getenv('scheduler_service_port')

app = Flask(__name__)

db = mongodb()

def get_app_instance_id():
    id = "AII_"+ str(int(time.time()))
    return id

@app.route('/schedule_application', methods=['POST'])
def scheduleapplication():
    try:
        all_details = request.get_json()
        app_instance_id = get_app_instance_id()
        first_start = parsedatetime(all_details['starttime'])
        first_stop = parsedatetime(all_details['endtime'])
        downtime = get_sec_in_json(all_details['interval'])
        # TODO: We can reduce some fields here using database reference
        new_schedule = Schedules(_id=app_instance_id,
                                 app_name=all_details['app_name'], 
                                 app_id=all_details['app_id'],
                                 next_start=first_start,
                                 next_stop=first_stop,
                                 uptime= (first_stop - first_start).total_seconds(),
                                 downtime=downtime,
                                 repetition=all_details['repetition'],
                                 sensors=json.dumps(all_details['sensors']))
        print("Sensor List: ",all_details['sensors'])

        new_schedule.save()
        send_log('INFO', f"Scheduled application {all_details['app_name']}:{all_details['app_id']}. Next start at {first_start}")
    except Exception as e:
        msg= "err_msg : " + str(e)
        rep ={
            "err_msg":msg
        }
        send_log('ERR', f"Could not scheduled application {all_details['app_name']}:{all_details['app_id']}. Reason: {msg}")
        return rep
    
    msg= "Scheduled!"
    rep={
        "succ_msg":msg,
        "AII":app_instance_id
    }
    return rep


def parsedatetime(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

def get_sec_in_json(j : dict) -> int:
    days = int(j.get('days', 0))
    hours = int(j.get('hours', 0))
    minutes = int(j.get('minutes', 0))
    seconds = int(j.get('seconds', 0))
    sec = seconds + (60 * (minutes + (60 * (hours + (24 * days)))))
    return sec


def send_to_deployment_service(action, services):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER_IP)

    if action not in ['start', 'stop']:
        producer.close()
        print("Invalid action :", action)
        send_log('WARN', f"Unknown action : {action}.")
        return
    if services.count()==0:
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
        send_log('INFO', f"Trying to {action} instance: {service._id} of app: {service.app_name}({service.app_id}).")
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

class ReSchedulingService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            bootstrap_server = [BOOTSTRAP_SERVER_IP]
            consumer = KafkaConsumer(
                KAFKA_RESCHEDULE_TOPIC,
                bootstrap_servers=bootstrap_server,
                # auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=GROUP_ID,
                value_deserializer=lambda x: loads(x.decode('utf-8')))

            for reschedule in consumer:
                print('Request to restart!!!')
                print(reschedule.value)
                try:
                    reschedule = reschedule.value
                    
                    instance = Schedules.objects.with_id(reschedule['instance_id'])
                    print(instance)
                    instance = [instance]
                    send_to_deployment_service('start', instance)
                except Exception as e:
                    send_log('ERR', str(e))
                    print(e)


if __name__ == "__main__":
    sched = SchedulingService()
    sched.start()
    re_sched = ReSchedulingService()
    re_sched.start()
    app.run(debug=False, port=PORT, host='0.0.0.0')