from flask import Flask, request
from dbconfig import *
import threading
from kafka import KafkaConsumer
from json import loads

import os
import dotenv
dotenv.load_dotenv()


app = Flask(__name__)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

db = mongodb()

class ReadLogs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        bootstrap_server = [BOOTSTRAP_SERVER_IP]
        consumer = KafkaConsumer(
            KAFKA_LOG_TOPIC,
            bootstrap_servers=bootstrap_server,
            # auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=GROUP_ID,
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        for log in consumer:
            print(log.value)
            try:
                log = log.value
                if log['type'] != 'heartbeat':
                    new_log = Logs(service_name=log['service_name'], msg=log['msg'], time=log['time'])
                    new_log.save()
            except Exception as e:
                print(e)

# {
#     'type':'not_heartbeat',
#     'service_name':'node_Manager',
#     'msg':'this is msg',
#     'time':'11:51'
# }

@app.route("/get_logs", methods=['POST'])
def home():
    service_name = request.json['service_name']
    logs = Logs.objects(service_name=service_name).to_json()
    return logs


if __name__ == "__main__":
    th = ReadLogs()
    th.start()
    app.run(host=HOST,port=PORT, debug=False)
