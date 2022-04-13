import mongoengine as db
import os
import dotenv
dotenv.load_dotenv()

database_name = 'monitoring_db'
mg_user = os.getenv('MONGODB_USER')
mg_pass = os.getenv('MONGODB_PASS') 
cluster = os.getenv('MONGODB_CLUSTER')
DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(mg_user,mg_pass , cluster,database_name)
 

class RegisteredServices(db.Document):
    service_id = db.StringField(Required=True)
    timestamp = db.StringField(Required=True)

    def to_json(self):
        return {
            "service_id": self.service_id,
            "timestamp":self.timestamp
        }

def mongodb():
    db.connect(host=DB_URI)
    return db