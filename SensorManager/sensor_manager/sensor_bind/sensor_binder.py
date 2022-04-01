from .sensor_bind_model import SensorBindModel
from .sensor_bind_model import Sensor_Used

from dbconfig import *
from util.constants import *
from mongoengine.queryset.visitor import Q
import jsonify
from datetime import datetime

def get_Val():
    dt = datetime.today()
    seconds = dt.timestamp()
    seconds=str(seconds)
    seconds = seconds.split(".")
    seconds=seconds[1]
    return seconds[-6:]

db = mongodb()
def reg_bind_sensor(request_data):
        sensor_bind_ids = {}
        for sensor_data in request_data['Details']:
            sp = sensor_data['port']
            if not SensorBindModel.objects.filter(Q(sensor_port=sp)):
                d1 = sensor_data['name']
                d2 = sensor_data['ip']
                d3 = sensor_data['port']
                d4 = sensor_data['loc']
                d5 = sensor_data['type']
                d6 = sensor_data['data_type']
                d7 = get_Val()
                conference_ = SensorBindModel(sensor_name=d1, sensor_ip=d2, sensor_port=d3, sensor_loc=d4, sensor_type=d5, sensor_data_type=d6, sensor_bind_id=d7)
                conference_.save()
                find2 = SensorBindModel.objects.filter(Q(sensor_port=sp)).first()
                sid = find2.sensor_bind_id
                sensor_bind_ids[find2.sensor_name] = (str)(sid)
                    # print(type(find2))
                    # return find2
            else:
                return "Port Already Exists"
        return sensor_bind_ids

    # except Exception as e:
    #     print(e)
    #     return "Failed to process", HTTP_INTERNAL_SERVER


# def (request_data):
#     try:
#         sensor_bind_ids = {}
#         for sensor_data in request_data['Details']:
#             sp=sensor_data['port']
#             find = bool(SensorBindModel.query.filter_by(
#                 sensor_port=sp).first())
#             if not find:
#  reg_bind_sensor               d1 = sensor_data['name']
#                 d2 = sensor_data['ip']
#                 d3 = sensor_data['port']
#                 d4 = sensor_data['loc']
#                 d5 = sensor_data['type']
#                 data = SensorBindModel(d1,d2,d3,d4,d5)
#                 db.session.add(data)
#                 db.session.commit()
#                 find2 = SensorBindModel.query.filter_by(
#                     sensor_port=sp).first()
#                 sid = find2.sensor_bind_id
#                 sensor_bind_ids[find2.sensor_name]=(str)(sid)
#                 # print(type(find2))
#                 # return find2
#             else:
#                 return "Port Already Exists"
#         return sensor_bind_ids

#     except Exception as e:
#         print(e)
#         return "Failed to process", HTTP_INTERNAL_SERVER

def Check(r_data):
    checked_sensor = {"ids":[]}
    flag=1
    for request_data in r_data["Details"]:
        loc = request_data['loc']
        stype = request_data['stype']
        find2 = SensorBindModel.objects.filter(
            Q(sensor_loc=loc) & Q(sensor_type=stype)).first()
        if(find2):
            checked_sensor['ids'].append()
        else:
           return "All sensors of given type are not present at the given location"
        # a = bool(SensorBindModel.query.filter_by(
        #     sensor_loc=loc, sensor_bind_id=sid).first())
        # if(a):
        #     s = "Sensor "+sid+" is present at provided location"
        #     checked_sensor[str(sid)] = s
        # else:
        #     s2 = "Sensor "+sid+" is not present at provided location"
        #     checked_sensor[str(sid)] = s2
    return checked_sensor


# def Check(r_data):
#     checked_sensor={}
#     for request_data in r_data["Details"]:
#         loc=request_data['loc']
#         sid=request_data['sid']
#         # find2 = SensorBindModel.objects.filter(
#         #     Q(sensor_loc=loc) sensor_bind_id=sid)).first()
#         a = bool(SensorBindModel.query.filter_by(sensor_loc=loc, sensor_bind_id = sid).first())
#         if(a):
#             s = "Sensor "+sid+" is present at provided location" 
#             checked_sensor[str(sid)] = s
#         else:
#             s2= "Sensor "+sid+" is not present at provided location"
#             checked_sensor[str(sid)] = s2
    
#     return checked_sensor

def start_sensor(val):

    pass


def sensor_add_db(val):
    conference_ = Sensor_Used(sensor_bind_id=val, number=1)
    conference_.save()


def sensor_add(val):
    Sensor_Used.objects(sensor_bind_id=val).update_one(inc__number=1)

    #         sensor_ = SensorBindModel.query.filter_by(sensor_port=sensor_data['sensor_port']).first()
    #         if not sensor_:
    #             sensor_obj = SensorBindModel(**sensor_data)
    #             try:
    #                 db.session.add(sensor_obj)
    #                 db.session.commit()
    #             except Exception as i:
    #                 print(i)
    #                 return jsonify(error="Failed"), HTTP_BAD_REQUEST

    #             db.session.refresh(sensor_obj)
    #             sensor_bind_ids.append(sensor_obj.sensor_bind_id)

    #         # api_response = requests.get(url="localhost:8081//service_lookup?service_name="+str(sensor_obj))
    #     return jsonify(data=sensor_bind_ids), HTTP_OK

    