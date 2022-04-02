
from json import loads
from time import sleep
from kafka import KafkaConsumer
from utilities.constants import kafka_url

def handle_deployment():
    try:
        consumer_data = KafkaConsumer(
            'app_deploy',
            bootstrap_servers=[kafka_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

        print(consumer_data)
        # if consumer_data['requesttype'] == 'start':
        #     deploy_models(consumer_data['models'])
        #     deploy_app(consumer_data['app'])
        # else:
        #     terminate_models(consumer_data['models'])
        #     terminate_app(consumer_data['app'])
        
    except Exception as e:
        print('Error in node_manager.handle_deployment', e)
