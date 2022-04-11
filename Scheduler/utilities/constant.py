import os
import dotenv
dotenv.load_dotenv()

BOOTSTRAP_SERVER_IP = os.getenv('kafka_bootstrap')

KAFKA_SCHEDULE_TOPIC = 'topic_schedule'
KAFKA_RESCHEDULE_TOPIC = 'service_dead_app'
SERVICE_NAME="Scheduler"
DATABASE_NAME = 'scheduler_db'
GROUP_ID = "scheduler_group_id"

AZURE_FILESHARE='fileshare'
AZURE_STORAGE_NAME='hack2storage'
AZURE_STORAGE_KEY='iVYu1uayUo9p0h3k00IdqMpLRX2rSZJ8kldu3cpA3AK6AZqPTuLxd9fmV9zGEmqSqtON0zrlCOTw+AStjdUEGQ=='
MONGODB_USER="kamal"
MONGODB_PASS='kamal123'
MONGODB_CLUSTER='cluster0.lzygp.mongodb.net'