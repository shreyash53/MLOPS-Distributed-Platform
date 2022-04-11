import mongoengine as db
import os
import dotenv
dotenv.load_dotenv()

database_name = 'SLCM_DB'
mduser = os.getenv('MONGODB_USER')
mdpass = os.getenv('MONGODB_PASS') 
cluster = os.getenv('MONGODB_CLUSTER')
kafka_bootstrap = os.getenv('kafka_bootstrap')

DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(mduser,mdpass , cluster,database_name)

print(kafka_bootstrap)

def mongodb():
    db.connect(host=DB_URI)
    return db

db = mongodb()

class slcm(db.Document):
    instance_id = db.StringField()
    service_type = db.StringField()
    service_name = db.StringField()
    state = db.StringField()
    service_ip = db.StringField()
    service_port = db.StringField()
    nodeid = db.StringField()
    def to_json(self):
        return {
            "instance_id":self.instance_id,
            "service_type": self.service_type,
            "service_name" : self.service_name,
            "state":self.state,
            "service_ip" : self.ip,
            "service_port":self.port,
            "nodeid":self.nodeid
        }

def savetodb(kwargs):
    try:
        data = slcm(**kwargs)
        data.save()
        return "success"
    except Exception as e: 
        return None


def fetchdb(kwargs):
    try:
        data = slcm.objects(**kwargs)[0]
        return data
    except Exception as e:
        return  None

def updatedb(kwargs,kwargs2):
    try:
        data = slcm.objects(**kwargs).update(**kwargs2)
        return "success"
    except Exception as e:
        return  None
    
def inc_service(name , stype):
    try :
        obj = slcm.objects(service_name = name,service_type =stype)
        cur = obj.usedby
        obj.update(useddby = cur+1)
        return "success"
    except Exception as e:
            return None

def dec_service(name , stype):
    try :
        obj = slcm.objects(service_name = name,service_type =stype)
        cur = obj.usedby
        obj.update(useddby = cur-1)
        return cur-1
    except Exception as e:
            return None