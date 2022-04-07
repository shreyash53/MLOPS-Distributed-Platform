import mongoengine as db
from utilities.constant import *

DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
        MONGODB_USER
        , MONGODB_PASS 
        , MONGODB_CLUSTER
        , DATABASE_NAME)


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

def mongodb():
    db.connect(host=DB_URI)
    return db