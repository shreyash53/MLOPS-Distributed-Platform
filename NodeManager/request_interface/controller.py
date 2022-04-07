from json import loads
from node_manager.model import RunningServices
from mongoengine.queryset.visitor import Q
from requests import post
from kafka import KafkaConsumer
from utilities.constants import SLCM_URL, kafka_url

consumer = KafkaConsumer(
    bootstrap_servers=[kafka_url],
    # auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

def build_url(model_):
    if model_.node.nodeUrl:
        return model_.node.nodeUrl
    return '{}:{}'.format(model_.node.nodeIpAddress, model_.node.nodePortNo)

def get_model_data(modelId, data):
    # model_ = RunningServices.objects.filter(
    #     Q(serviceId = modelId) &
    #     Q(serviceType = 'model')
    # )
    response = post(SLCM_URL, json={
        "service_id" : modelId,
        "service_type" : "model"
    })
    if not response.status_code == 200:
        print('No model found')
        return "No data"
    response = response.json()
    # url = build_url(model_.first())
    url = response['url']
    return post('{}/get_result'.format(url), json=data).json()


def get_sensor_data(sensor_build_id):
    try:
        sensor_topic = 'S_{}'.format(sensor_build_id)
        consumer.subscribe([sensor_topic])
        print('connection successfull')
        for data in consumer:
            print('data recieved in sensor', data.value)
            return data.value
        # msg = consumer.poll(2)
        # print(msg)
        # return msg
    except Exception as e:
        print('Error in request_interface.get_sensor_data', e)