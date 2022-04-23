from json import loads

from kafka import KafkaConsumer

from utilities.constants import kafka_url
from .deployment import deployment_handler
from .terminate import termination_handler
import sys

def consumer_logic(consumer_data):
    print(consumer_data)
    consumer_data = consumer_data.value
    data = consumer_data['data']
    if consumer_data['requesttype'] == 'start':
        deployment_handler(consumer_data['servicetype'], data)
    else:
        termination_handler(consumer_data['servicetype'], data)


def consumer_thread():
    while True:
        try:
            consumer = KafkaConsumer(
                sys.argv[2],
                bootstrap_servers=[kafka_url],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-group',
                value_deserializer=lambda x: loads(x.decode('utf-8'))
            )
            print('inside consumer_thread')
            for data in consumer:
                consumer_logic(data)

            # if consumer_data['requesttype'] == 'start':
            #     deploy_models(consumer_data['models'])
            #     deploy_app(consumer_data['app'])
            # else:
            #     terminate_models(consumer_data['models'])
            #     terminate_app(consumer_data['app'])

        except Exception as e:
            print('Error in node_manager.consumer_thread', e)
