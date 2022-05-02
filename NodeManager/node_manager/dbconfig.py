import mongoengine as db
import os
import dotenv
dotenv.load_dotenv()

database_name = 'requestmanager_db'
mduser = os.getenv('MONGODB_USER')
mdpass = os.getenv('MONGODB_PASS') 
cluster = os.getenv('MONGODB_CLUSTER')
DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(mduser,mdpass , cluster,database_name)


def mongodb():
    print(DB_URI)
    db.connect(host=DB_URI)
    
    return db