import os
import dotenv

dotenv.load_dotenv()

database_name = 'child_node_db'
DB_URI = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
    os.environ.get('MONGODB_USER'), os.environ.get('MONGODB_PASS'), os.environ.get('MONGODB_CLUSTER'),database_name)
