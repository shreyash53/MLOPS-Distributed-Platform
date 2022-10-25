import mongoengine as db
from BootstrapService.utilities.constant import *

DB_URI ='mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
        MONGODB_USER
        , MONGODB_PASS 
        , MONGODB_CLUSTER
        , DATABASE_NAME)


class Bootstrap(db.Document):
    service_name = db.StringField(required=True)
    contrainer_id = db.StringField(required=True)


def mongodb():
    db.connect(host=DB_URI)
    return db