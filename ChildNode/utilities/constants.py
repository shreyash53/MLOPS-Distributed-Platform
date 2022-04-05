
static_ip = '0.0.0.0'
static_port = '6100'
# kafka_ip = 'localhost'
kafka_ip = '20.219.107.251'
kafka_port = '9092'
kafka_url = "{0}:{1}".format(kafka_ip, kafka_port)
# node_model = 'node_model'
# node_app = 'node_app'
POST = ['POST']
GET = ['GET']

APP_DIR = '/home/shreyash/data/app'
MODEL_DIR = '/home/shreyash/data/model'

AZURE_MODEL_PATH = 'root/UserData/Models'

SLCM_TOPIC_NAME = 'register'

CHILD_NODE_IP = 'http://192.168.180.153'
CHILD_NODE_URL = '{}:6000'.format(CHILD_NODE_IP)