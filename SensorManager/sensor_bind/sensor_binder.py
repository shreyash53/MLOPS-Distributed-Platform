from .sensor_bind_model import SensorBindModel
from .sensor_bind_model import SensorRegisterModel
from .sensor_bind_model import Sensor_Used
from log_generator import send_log
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

def reg_sensor(request_data):
    try:
        for sensor_data in request_data['Details']:
            tp=sensor_data['type']
            d_tp=sensor_data['data_type']
            if not SensorRegisterModel.objects.filter(Q(sensor_type=tp) & Q(sensor_data_type=d_tp)):
                conference_ = SensorRegisterModel(sensor_type=tp, sensor_data_type=d_tp)
                conference_.save()
                send_log("INFO","Sensor Registered Successfully")
                return "Successful"
            else:
                send_log("WARN","This type and data type already exists")
                return "This type and data type already exists"
    except:
        send_log("ERR","Failed to process")
        return "Failed to process", HTTP_INTERNAL_SERVER

def reg_bind_sensor(request_data):
    try:  
        # sensor_bind_ids = {}
        for sensor_data in request_data['Details']:
            sp = sensor_data['port']
            sip= sensor_data['ip']
            if not SensorBindModel.objects.filter(Q(sensor_port=sp) & Q(sensor_ip=sip)):
                if (SensorRegisterModel.objects.filter(Q(sensor_type=sensor_data['type']) & Q(sensor_data_type=sensor_data['data_type']))):
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
                    ll=str(is_sensor)+" "+str(IP)+" "+str(Port)+" "+str(topic_name)
                    send_log("INFO",ll)
                    if(is_sensor):
                        t1 = threading.Thread(target=fun, args=(topic_name, IP, Port,time))
                        threads.append(t1)
                        t1.start()
                    else:
                        t2 = threading.Thread(target=fun2, args=(topic_name, IP, Port,time))
                        threads.append(t2)
                        t2.start()
                else:
                    send_log("WARN","No such sensor type and sensor data type exists on our platform")
                    return "No such sensor type and sensor data type exists on our platform"
            else:
                send_log("WARN","This IP:PORT Already Exists")
                return "This IP:PORT Already Exists"
        return "Successful" 
        # return sensor_bind_ids

    except Exception as e:
        send_log("ERR",e)
        # print(e)
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
        ll=str(is_sensor)+" "+str(IP)+" "+str(Port)+" "+str(topic_name)
        send_log("INFO",ll)
        # print(is_sensor, IP, Port, topic_name)
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
    for sensor in SensorRegisterModel.objects:
        print(sensor.sensor_type, sensor.sensor_data_type)
        if ((sensor.sensor_type, sensor.sensor_data_type)) not in auxiliaryList:
            auxiliaryList.append((sensor.sensor_type, sensor.sensor_data_type))
    # send_log("INFO",)
    # print(auxiliaryList)
    return auxiliaryList

    

def Check_Valss():
    auxiliaryList = []
    for sensor in SensorBindModel.objects:
        a = (sensor.sensor_type, sensor.sensor_data_type,
             sensor.sensor_loc, sensor.sensor_bind_id,sensor.sensor_name)
        if len(auxiliaryList)==0:
            x = []
            x.append(a[0])
            x.append(a[1])
            y = []
            y.append((a[2], a[3],a[4]))
            x.append(y)
            auxiliaryList.append(x)
        else:
            for i in range(len(auxiliaryList)):
                if a[0] == auxiliaryList[i][0] and a[1] == auxiliaryList[i][1]:
                    f=0
                    for j in range(len(auxiliaryList[i][2])):
                        if a[2] == auxiliaryList[i][2][0] and a[3] == auxiliaryList[i][2][1]:
                            f=1
                    if(f==0):
                        # print("Old: ",(a[2],a[3]))
                        auxiliaryList[i][2].append((a[2],a[3],a[4]))
                else:
                    s=0
                    for k in range(len(auxiliaryList)):
                        if a[0] == auxiliaryList[k][0] and a[1] == auxiliaryList[k][1]:
                            s=1
                    if s==0:
                        x=[]
                        x.append(a[0])
                        x.append(a[1])
                        y=[]
                        y.append((a[2],a[3],a[4]))
                        x.append(y)
                        # print ("New: ", x)
                        auxiliaryList.append(x)
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

def Get_Location(Request_Data):
    main_dic=[]
    for sensor in Request_Data["details"]:
        sid=[]
        for sen in SensorBindModel.objects:
            if sen.sensor_type==sensor['sensortype'] and sen.sensor_data_type==sensor['sensordatatype']:    
                flag=0
                for loc in sid:
                    if loc['loc']==sen.sensor_loc:
                        flag=1
                if(flag==0):
                    dic={}
                    dic['sensor_bind_id']=sen.sensor_bind_id
                    dic['loc']=sen.sensor_loc
                    sid.append(dic)    
        main_dic.append({"type":sensor['sensortype'],"datatype":sensor['sensordatatype'],"locations":sid})    # print(flag," ",error," ",sid)
    return main_dic





