from kafka import KafkaConsumer
from json import loads
from dbconfig import *


if __name__ == "__main__":
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