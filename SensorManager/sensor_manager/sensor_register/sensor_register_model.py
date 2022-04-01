from sensor_config import db

class Sensor_Register(db.Model):
    __tablename__ = 'Sensor_Register'
    sensor_name = db.Column(db.String(64), primary_key=True)
    sensor_type = db.Column(db.String(64), index=True)

    def __init__(self,  sensor_name, sensor_type):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type