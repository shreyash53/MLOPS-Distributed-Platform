import mongoengine as db
import os
import dotenv
dotenv.load_dotenv()

database_name = 'logging_db'
mg_user = os.getenv('MONGODB_USER')
mg_pass = os.getenv('MONGODB_PASS') 
cluster = os.getenv('MONGODB_CLUSTER')
DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(mg_user,mg_pass , cluster,database_name)


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