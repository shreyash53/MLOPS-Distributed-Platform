from email.policy import default
from xmlrpc.client import Boolean
from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField, URLField, ListField, DictField, DateTimeField
import datetime

class SensorBindModel(Document):

    sensor_bind_id = StringField() 
    sensor_name = StringField()
    sensor_loc = StringField()
    sensor_ip = StringField()
    sensor_type = StringField()
    sensor_port = IntField()
    sensor_data_type = StringField()
    is_sensor = IntField()
    time_in_sec=IntField()

    def getObject(self):
        obj = {
            "sensor_name":self.sensor_name,
            "sensor_ip": self.sensor_ip,        
            "sensor_port": self.sensor_port,
            "sensor_loc": self.sensor_loc,  
            "sensor_type": self.sensor_type,
            "sensor_data_type": self.sensor_data_type,
            "sensor_bind_id": self.sensor_bind_id,
            "is_sensor": self.is_sensor,
            "time_in_sec":self.time_in_sec
        }
        return obj


# class SensorBindModel(db.Model):
#     sensor_bind_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     sensor_name = db.Column(db.String(50))
#     sensor_loc = db.Column(db.String(50))
#     sensor_ip = db.Column(db.String(50))
#     sensor_type = db.Column(db.String(50))
#     sensor_port = db.Column(db.Integer)

#     def __init__(self,  sensor_name, sensor_ip, sensor_port, sensor_loc,sensor_type):
#         self.sensor_name = sensor_name
#         self.sensor_ip = sensor_ip
#         self.sensor_port = sensor_port
#         self.sensor_loc = sensor_loc
#         self.sensor_type = sensor_type

class Sensor_Used(Document):
    sensor_bind_id = IntField(primary_key=True)
    number = IntField()

    def getObject(self):
        obj = {
            "sensor_bind_id": self.sensor_bind_id,
            "number": self.number
        }
        return obj


# class Sensor_Used(db.Model):
#     sensor_bind_id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer)

