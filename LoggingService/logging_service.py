from flask import Flask, request
from dbconfig import *
import threading
from kafka import KafkaConsumer
import datetime
from json import loads
import os
import dotenv
dotenv.load_dotenv()

PORT = os.getenv('logging_service_port')


app = Flask(__name__)

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
                now = datetime.datetime.now()
                new_log = Logs(log_type=log['type'], 
                                service_name=log['service_name'], 
                                msg=log['msg'], 
                                time=now)
                new_log.save()
            except Exception as e:
                print(e)


def parsedatetime(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

def get_logs_bw(starttime, endtime, service_name, page_no):
    res = Logs.objects(time__lte=endtime, 
                        time__gt=starttime, 
                        service_name=service_name)
    total_records = res.count()
    next_page = None
    last_record = total_records//PER_PAGE_RECORD
    if next_page < last_record:
        next_page = page_no + 1
    offset = (page_no - 1) * PER_PAGE_RECORD
    res = res.skip(offset).limit(PER_PAGE_RECORD)
    data = {'result':res, 'next_page':next_page}
    return data


@app.route("/get_logs", methods=['GET','POST'])
def home():
    req = request.json
    service_name = req['service_name']
    log_type = req['type']
    logs_from = parsedatetime(req['start_time'])
    logs_to = parsedatetime(req['end_time'])
    page_no = int(req['page'])

    if log_type == 'ALL':
        logs = Logs.objects().to_json()
        return logs

    return get_logs_bw(starttime=logs_from,
                        endtime=logs_to,
                        service_name=service_name,
                        page_no=page_no)


if __name__ == "__main__":
    th = ReadLogs()
    th.start()
    app.run(debug=False, port=PORT, host='0.0.0.0')
