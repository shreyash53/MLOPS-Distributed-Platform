import mongoengine as db
from utilities.constant import *

DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
        MONGODB_USER
        , MONGODB_PASS 
        , MONGODB_CLUSTER
        , DATABASE_NAME)


class Logs(db.Document):
    service_name = db.StringField()
    msg = db.StringField()
    time = db.StringField()

    def to_json(self):
        return {
            "service_name": self.service_name,
            "msg":self.msg,
            "time":self.time
        }

def mongodb():
    db.connect(host=DB_URI)
    return db