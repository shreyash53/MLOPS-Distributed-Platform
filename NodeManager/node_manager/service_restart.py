


from json import loads
from kafka import KafkaConsumer
from node_manager.deployment import deploy_model
from utilities.constants import kafka_url

def restart_model_consumer():
    try:
        consumer = KafkaConsumer(
            'model_restart',
            bootstrap_servers=[kafka_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group-2',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        print('inside nodemanager consumer thread')
        for data in consumer:
            deploy_model(data.value)


    except Exception as e:
        print('Error in node_manager.consumer_thread', e)
