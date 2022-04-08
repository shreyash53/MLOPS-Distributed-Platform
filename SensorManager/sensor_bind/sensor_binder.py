from .sensor_bind_model import SensorBindModel
from .sensor_bind_model import Sensor_Used
from .Get_Service import *
from dbconfig import *
from util.constants import *
from mongoengine.queryset.visitor import Q
import jsonify
from datetime import datetime
import threading
threads=[]
def get_Val():
    dt = datetime.today()
    seconds = dt.timestamp()
    seconds=str(seconds)
    seconds = seconds.split(".")
    seconds=seconds[1]
    return seconds[-6:]

db = mongodb()
def reg_bind_sensor(request_data):
    try:  
        # sensor_bind_ids = {}
        for sensor_data in request_data['Details']:
            sp = sensor_data['port']
            sip= sensor_data['ip']
            if not SensorBindModel.objects.filter(Q(sensor_port=sp) & Q(sensor_ip=sip)):
                d1 = sensor_data['name']
                d2 = sensor_data['ip']
                d3 = sensor_data['port']
                d4 = sensor_data['loc']
                d5 = sensor_data['type']
                d6 = sensor_data['data_type']
                d7 = get_Val()
                # d7="1"
                d8 =sensor_data['is_sensor']
                d9 = sensor_data['time_in_sec']
                conference_ = SensorBindModel(sensor_name=d1, sensor_ip=d2, sensor_port=d3, sensor_loc=d4, sensor_type=d5, sensor_data_type=d6, sensor_bind_id=d7, is_sensor=d8, time_in_sec=d9)
                conference_.save()
                # print("HEllo")
                find2 = SensorBindModel.objects.filter(
                    Q(sensor_port=sp) & Q(sensor_ip=sip)).first() 
                is_sensor = find2.is_sensor
                topic_name = "S_"+str(find2.sensor_bind_id)
                IP = find2.sensor_ip
                Port = find2.sensor_port
                time= find2.time_in_sec
                print(is_sensor, IP, Port, topic_name)
                if(is_sensor):
                    t1 = threading.Thread(target=fun, args=(topic_name, IP, Port,time))
                    threads.append(t1)
                    t1.start()
                else:
                    t2 = threading.Thread(target=fun2, args=(topic_name, IP, Port,time))
                    threads.append(t2)
                    t2.start()
            else:
                return "This IP:PORT Already Exists"
        return "Successful" 
        # return sensor_bind_ids

    except Exception as e:
        print(e)
        return "Failed to process", HTTP_INTERNAL_SERVER

# def Check(r_data):
#     checked_sensor = {"ids":[]}
#     flag=1
#     for request_data in r_data["Details"]:
#         loc = request_data['loc']
#         stype = request_data['stype']
#         find2 = SensorBindModel.objects.filter(
#             Q(sensor_loc=loc) & Q(sensor_type=stype)).first()
#         if(find2):
#             checked_sensor['ids'].append()
#         else:
#            return "All sensors of given type are not present at the given location"

#     return checked_sensor


def Start_Services():
    Ob=SensorBindModel.objects.all()
    for find2 in Ob:
        is_sensor = find2.is_sensor
        topic_name = "S_"+str(find2.sensor_bind_id)
        IP = find2.sensor_ip
        Port = find2.sensor_port
        time = find2.time_in_sec
        print(is_sensor, IP, Port, topic_name)
        if(is_sensor):
            t1 = threading.Thread(target=fun, args=(topic_name, IP, Port, time))
            threads.append(t1)
            t1.start()
        else:
            t2 = threading.Thread(target=fun2, args=(topic_name, IP, Port, time))
            threads.append(t2)
            t2.start()
    return "Success"


def start_sensor(find2,x):
    topic_name = "S_"+str(find2.sensor_bind_id)
    IP = find2.sensor_ip
    Port=find2.sensor_port
    is_sensor = find2.is_sensor
    if(is_sensor):
        fun(topic_name,IP,Port)
    else:
        fun2(topic_name, IP, Port)

def sensor_add_db(val):
    conference_ = Sensor_Used(sensor_bind_id=val, number=1)
    conference_.save()


def sensor_add(val):
    Sensor_Used.objects(sensor_bind_id=val).update_one(inc__number=1)

def Check_Vals():
    auxiliaryList = []
    for sensor in SensorBindModel.objects:
        a = (sensor.sensor_type, sensor.sensor_data_type)
        print(a)
        if a not in auxiliaryList:
            auxiliaryList.append(a)
    return auxiliaryList

def Check_From_Dev(Request_Data):
    error=[]
    flag=0
    for sensor in Request_Data["Details"]:
        a=SensorBindModel.objects.filter(Q(sensor_type=sensor["sensortype"]) & Q(
            sensor_data_type=sensor['sensordatatype'])).first()
        if not a:
            error.append(sensor['sensorid'])
            flag=1
        return flag,error

def Check_From_Runner(Request_Data):
    error=[]
    sid=[]
    flag=0
    i=0
    print("Sensor Request Details: ",Request_Data['Details'])
    for sensor in Request_Data["Details"]:
        a=SensorBindModel.objects.filter(Q(sensor_type=sensor['Sensor_Type']) & Q(
            sensor_loc=sensor['Sensor_loc'])).first()
        # print(a.sensor_loc,"line 126")
        if not a:
            error.append(i)
            flag=1
        else:
            dic={}
            dic['sensor_bind_id']=a.sensor_bind_id
            dic['sensor_name']=a.sensor_name
            sid.append(dic)
        i+=1
    # print(flag," ",error," ",sid)
    return flag,error,sid





