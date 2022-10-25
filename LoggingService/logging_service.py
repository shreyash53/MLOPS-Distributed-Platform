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
    if date_time_str == 'ALL' or date_time_str ==  '':
        return 'ALL'
    date_time_str=date_time_str[8:10]+"/"+date_time_str[5:7]+"/"+date_time_str[2:4]+" "+date_time_str[11:13]+":"+date_time_str[14:16]+":00"
    print("TIME:",date_time_str)
    return datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

def get_logs_bw(starttime, endtime, service_name, page_no):
    res = Logs.objects(time__lte=endtime, 
                        time__gt=starttime, 
                        service_name=service_name)
    total_records = res.count()
    next_page = None
    prev_page = None
    last_record = total_records//PER_PAGE_RECORD
    if page_no < last_record:
        next_page = page_no + 1
    if page_no > 1:
        prev_page = page_no -1
    offset = (page_no - 1) * PER_PAGE_RECORD
    res = res.skip(offset).limit(PER_PAGE_RECORD)
    data = {'result':res, 'next':next_page, 'prev':prev_page}
    return data

def get_services_name():
    services=[]
    services.append(os.environ.get('monitoring_service_name'))
    services.append(os.environ.get('SLCM_service_name'))
    services.append(os.environ.get('node_manager_service_name'))
    services.append(os.environ.get('sensor_manager_service_name'))
    services.append(os.environ.get('request_manager_service_name'))
    services.append(os.environ.get('scheduler_service_name'))
    services.append(os.environ.get('logging_service_name'))
    services.append(os.environ.get('notification_manager_service_name'))
    services.append(os.environ.get('deployer_service_name'))
    services.append(os.environ.get('child_node_service_name'))
    return services

@app.route("/get_logs", methods=['GET','POST'])
def home():
    req = request.json
    print("logs_from:",req['start_time'])
    print("logs_to:",req['end_time'])
    service_name = req['service_name']
    log_type = req['type']
    logs_from = parsedatetime(req['start_time'])
    logs_to = parsedatetime(req['end_time'])
    page_no = int(req['page'])

    # if service_name=='ALL' and log_type=='ALL' and logs_from=='ALL':
    #     total_records = Logs.objects.count()
    #     next_page = None
    #     prev_page = None
    #     last_record = total_records//PER_PAGE_RECORD
    #     if page_no < last_record:
    #         next_page = page_no + 1
    #     if page_no > 1:
    #         prev_page = page_no -1
    #     offset = (page_no - 1) * PER_PAGE_RECORD
    #     print("###########################\n\n\n\n####################",Logs.objects())
    #     return {
    #     'result' : [{'msg':i.msg,'type':i.log_type,'service_name':i.service_name,'time':i.time} for i in Logs.objects().skip(offset).limit(PER_PAGE_RECORD)],
    #     'next' : next_page,
    #     'prev' : prev_page
    #     }
    query = dict()
    if service_name != 'ALL':
        query["service_name"] = service_name

    if log_type != 'ALL':
        query["log_type"] = log_type
    if logs_from != 'ALL' and logs_from!='':
        query["time__gte"] = logs_from
        query["time__lte"] = logs_to

    res = Logs.objects(**query)
    total_records = len(res)
    next_page = None
    prev_page = None
    if total_records%PER_PAGE_RECORD == 0:
        last_record = total_records//PER_PAGE_RECORD
    else:
        last_record = total_records//PER_PAGE_RECORD+1
    if page_no < last_record:
        next_page = page_no + 1
    if page_no > 1:
        prev_page = page_no -1
    offset = (page_no - 1) * PER_PAGE_RECORD
    res = res.skip(offset).limit(PER_PAGE_RECORD)
    print('LAST_RECORD:',total_records)
    print("\n\n\n\n-----------------------------",len(res))
    return {
        'result' : [{'msg':i.msg,'type':i.log_type,'service_name':i.service_name,'time':i.time} for i in res],
        'next' : next_page,
        'prev' : prev_page
    }
    # if log_type == 'ALL':
    #     logs = Logs.objects().to_json()
    #     return logs

    # return get_logs_bw(starttime=logs_from,
                        # endtime=logs_to,
                        # service_name=service_name,
                        # page_no=page_no)


if __name__ == "__main__":
    th = ReadLogs()
    th.start()
    app.run(debug=False, port=PORT, host='0.0.0.0')
