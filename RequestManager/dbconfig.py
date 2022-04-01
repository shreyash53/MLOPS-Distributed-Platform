import mongoengine as db
import os
import dotenv
dotenv.load_dotenv()

database_name = 'test'
DB_URI = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
    os.get.environ('MONGODB_CLUSTER'), os.get.environ('MONGODB_USER'), os.get.environ('MONGODB_PASS'), database_name)


def mongodb():
    db.connect(host=DB_URI)
    return db
