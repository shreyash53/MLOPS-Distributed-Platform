import threading
import os
from flask import Flask
# from json import dumps
from json import loads
# from time import sleep
from mongoengine.fields import *
from kafka import KafkaConsumer
from .dbconfig import mongodb
from .model import NodeDocument

# class consuming_load_balancing(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

def min_load_balance():
    # db=mongodb()
    try:
        consumer = KafkaConsumer(
            'load_balancer',
            bootstrap_servers=[os.getenv('kafka_bootstrap')],
            # auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        for message in consumer:
            cpu_usage=message.get("cpu_load")
            ram_usage=message.get("ram_load")
            nodeid=message.get("id")

            NodeDocument.objects(nodeName=nodeid).update(node_cpu_usage=cpu_usage,node_ram_usage=ram_usage)
        # node_manager_db.objects(nodeName=nodeid).update(node_ram_usage=ram_usage)
        # NodeDocument.save()
    except Exception as e:
        print('Error in fetching min load value', e)



# if __name__ == "__main__":
#     # db=mongodb()
#     x = consuming_load_balancing()
#     x.start()
