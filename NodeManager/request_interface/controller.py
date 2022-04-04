from json import loads
from node_manager.model import RunningServices
from mongoengine.queryset.visitor import Q
from requests import post
from kafka import KafkaConsumer
from utilities.constants import kafka_url

def build_url(model_):
    if model_.node.nodeUrl:
        return model_.node.nodeUrl
    return '{}:{}'.format(model_.node.nodeIpAddress, model_.node.nodePortNo)

def get_model_data(modelId, data):
    model_ = RunningServices.objects.filter(
        Q(serviceId = modelId) &
        Q(serviceType = 'model')
    )
    if not model_:
        print('No model found')
        return "No data"
    
    url = build_url(model_)
    return post('{}/get_result'.format(url), json=data).json()


def get_sensor_data(sensor_build_id):
    try:
        sensor_topic = 's_{}'.format(sensor_build_id)
        consumer = KafkaConsumer(
            sensor_topic,
            bootstrap_servers=[kafka_url],
            # auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

        for data in consumer:
            return data.value

    except Exception as e:
        print('Error in request_interface.get_sensor_data', e)