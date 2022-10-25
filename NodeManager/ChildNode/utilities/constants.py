from os.path import expanduser, join
import os
import dotenv
dotenv.load_dotenv()

USER_NAME = os.environ.get('USER')
static_ip = '0.0.0.0'
static_port = '5000'
# kafka_ip = 'localhost'
# kafka_ip = '20.219.107.251'
# kafka_port = '9092'
# kafka_url = "{0}:{1}".format(kafka_ip, kafka_port)
kafka_url = os.getenv("kafka_bootstrap")
# node_model = 'node_model'
# node_app = 'node_app'
POST = ['POST']
GET = ['GET']

# APP_DIR = '/home/shreyash/data/app'
# MODEL_DIR = '/home/shreyash/data/model'
# USER_DIR = expanduser('~/')
USER_DIR = f'/home/{USER_NAME}/'
APP_DIR = join(USER_DIR, 'Downloads', 'data', 'apps')
MODEL_DIR = join(USER_DIR, 'Downloads', 'data', 'models')

AZURE_MODEL_PATH = 'root/UserData/Models'

SLCM_TOPIC_NAME = 'register'

# CHILD_NODE_IP = 'http://192.168.178.153'
CHILD_NODE_IP = f"http://{os.environ.get('node_manager_service_ip')}"
CHILD_NODE_URL = f"{CHILD_NODE_IP}:{os.environ.get('node_manager_service_port')}"

# MY_IP = 'http://192.168.178.153:6201'
MY_IP = f'http://{os.environ.get("child_node_service_ip")}'

MONITOR_IP = f'http://{os.environ.get("monitoring_service_ip")}'
MONITOR_PORT = os.environ.get("monitoring_service_port")