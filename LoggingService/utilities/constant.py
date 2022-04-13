import os
import dotenv
dotenv.load_dotenv()

BOOTSTRAP_SERVER_IP = os.getenv('kafka_bootstrap')

KAFKA_LOG_TOPIC = 'logs'
SERVICE_NAME="Logging"
DATABASE_NAME = 'logging_db'
GROUP_ID = 'logging'

AZURE_FILESHARE='fileshare'
AZURE_STORAGE_NAME='hack2storage'
AZURE_STORAGE_KEY='iVYu1uayUo9p0h3k00IdqMpLRX2rSZJ8kldu3cpA3AK6AZqPTuLxd9fmV9zGEmqSqtON0zrlCOTw+AStjdUEGQ=='
MONGODB_USER="kamal"
MONGODB_PASS='kamal123'
MONGODB_CLUSTER='cluster0.lzygp.mongodb.net'