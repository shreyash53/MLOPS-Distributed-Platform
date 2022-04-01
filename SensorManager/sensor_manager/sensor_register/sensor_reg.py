from .sensor_register_model import Sensor_Register
from sensor_config import db
from util.constants import *

def reg_sensor(request_data):

    sensor_name = request_data['name']
    sensor_type = request_data['type']
    data = Sensor_Register(sensor_name, sensor_type)
    db.session.add(data)
    db.session.commit()
    return "Registered Successfully"
