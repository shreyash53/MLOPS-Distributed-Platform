import os
import dotenv
dotenv.load_dotenv()

BOOTSTRAP_SERVER_IP = os.getenv('kafka_bootstrap')

KAFKA_LOG_TOPIC = os.getenv('KAFKA_LOG_TOPIC')
SERVICE_NAME= os.getenv('logging_service_name')
DATABASE_NAME = 'logging_db'
GROUP_ID = 'logging'

AZURE_FILESHARE=os.getenv('AZURE_FILESHARE')
AZURE_STORAGE_NAME=os.getenv('AZURE_STORAGE_NAME')
AZURE_STORAGE_KEY=os.getenv('AZURE_STORAGE_KEY')
MONGODB_USER=os.getenv('MONGODB_USER')
MONGODB_PASS=os.getenv('MONGODB_PASS')
MONGODB_CLUSTER=os.getenv('MONGODB_CLUSTER')

PER_PAGE_RECORD = 10