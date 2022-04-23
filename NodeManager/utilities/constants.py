
import os
import dotenv
dotenv.load_dotenv()

SLCM_URL = "http://"+os.getenv('SLCM_service_ip')+":"+os.getenv('SLCM_service_port')

static_ip = '0.0.0.0'
static_port = os.getenv('node_manager_service_port')
# kafka_ip = 'localhost'
# kafka_ip = '20.219.107.251'
# kafka_port = '9092'
# kafka_url = "{0}:{1}".format(kafka_ip, kafka_port)
kafka_url = os.getenv("kafka_bootstrap")
node_model = 'node_model'
node_app = 'node_app'
POST = ['POST']
GET = ['GET']
HTTP_OK_STATUS_CODE = 200
# SLCM_URL = 'http://192.168.178.153:9000'