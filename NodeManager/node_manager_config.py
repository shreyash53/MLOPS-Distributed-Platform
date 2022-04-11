import os
import dotenv

dotenv.load_dotenv()

database_name = 'node_manager_db'
DB_USER_NAME = os.environ.get('MONGODB_USER')
DB_PASSwORD = os.environ.get('MONGODB_PASS')
DB_URI = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
    os.environ.get('MONGODB_USER'), os.environ.get('MONGODB_PASS'), os.environ.get('MONGODB_CLUSTER'),database_name)
