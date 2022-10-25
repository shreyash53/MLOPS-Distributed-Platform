from sensor_manager import app
import os
from dotenv import load_dotenv

load_dotenv()

SENSOR_MGR_PORT = os.getenv('sensor_manager_service_port')
