import threading
import os
import psutil
import json
from flask import Flask
from json import dumps
from json import loads
from time import sleep
from ChildNode.child_node_config import NODE_ID

from kafka import KafkaProducer


def sending_load():
    
    while(True):
        try:
            producer = KafkaProducer(bootstrap_servers=[os.getenv('kafka_bootstrap')],
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))
            load1, load5, load15 = psutil.getloadavg()
            cpu_usage = (load1/os.cpu_count()) * 100
            
            ram_usage=psutil.virtual_memory().percent
            
            id=NODE_ID
            msg={
                "cpu_load":cpu_usage,
                "ram_load":ram_usage,
                "id":id
            }
            producer.send('load_balance',value=msg)
            # sleep(10)

        except Exception as e:
            print('Error in sending load in kafka', e)
        
        sleep(10)



# if __name__ == "__main__":
#     x = uploading_load_balancing()
#     x.start()