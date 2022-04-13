import os
import dotenv
dotenv.load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("kafka_bootstrap")
KAFKA_SCHEDULE_TOPIC = 'schedule'
AZURE_ROOT_PATH = 'root'
AZURE_PLATFORM_PATH = 'root/PlatformFile'
AZURE_APP_PATH = 'root/UserData/AppData'
AZURE_MODEL_PATH = 'root/UserData/Models'

