import os
import dotenv
dotenv.load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("kafka_bootstrap")

# BOOTSTRAP_SERVERS = '20.219.107.251:9092'
KAFKA_SCHEDULE_TOPIC = 'schedule'