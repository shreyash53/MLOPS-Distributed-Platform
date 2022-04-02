import mongoengine as db
import os
from dotenv import load_dotenv
load_dotenv()

default_name = 'test'

DB_URI = 'mongodb+srv://{}:{}@{}/'.format(
    os.environ.get('MONGODB_USER'), os.environ.get('MONGODB_PASS'), os.environ.get('MONGODB_CLUSTER'))


def mongodb():
    db.connect(db=default_name, alias="default", host=DB_URI)
    return db