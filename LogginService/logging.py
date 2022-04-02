from crypt import methods
import readline
from flask import Flask, request, render_template
from dbconfig import *
import threading
from kafka import KafkaConsumer
from json import loads


app = Flask(__name__)
HOST = '0.0.0.0'
PORT = '8008'

db = mongodb()

class ReadLogs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        db = mongodb()
        topic_name = 'logs'
        kafka_server_ip = 'localhost:9092'
        group_id = 'logging'
        bootstrap_server = [kafka_server_ip]
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_server,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        for log in consumer:
            try:
                log = log.value
                if log['type'] != 'heartbeat':
                    new_log = Logs(service_name=log['service_name'], msg=log['msg'], time=log['time'])
                    new_log.save()
            except Exception as e:
                print(e)


@app.route("/get_logs", methods=['POST'])
def home():
    service_name = request.json['service_name']
    logs = Logs.objects(service_name=service_name).to_json()
    return logs


if __name__ == "__main__":
    th = ReadLogs()
    th.start()
    app.run(host=HOST,port=PORT, debug=True)
