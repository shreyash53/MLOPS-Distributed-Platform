

from json import dumps
from time import sleep

from node_manager.model import NodeDocument
from utilities.constants import kafka_url, node_app, node_model, SLCM_URL
from kafka import KafkaProducer
from requests import post

def build_request_data(request_type, service_type, data, all_data=None):
    if service_type == 'app':
        return {
            "requesttype" : request_type,
            "servicetype" : service_type,
            "data" : {
                'app_data' : data,
                "sensor_data" : all_data['sensors'],
                "models_data" : all_data['models']
            }
        }
    return {
        "requesttype" : request_type,
        "servicetype" : service_type,
        "data" : data
    }

def send_using_kafka(topic_name, data):
    producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    producer.send(topic_name, data)
    sleep(2)


def find_appropriate_node(node_type):
    nodes = NodeDocument.objects.filter(nodeType=node_type)
    if not nodes:
        print('Kindly add some nodes of type', node_type)
        return
    node = nodes.first()
    return node


def deploy_model(model_to_deploy):
    try:
        node = find_appropriate_node(node_model)
        if not node:
            return
        
        send_using_kafka(node.nodeKafkaTopicName, build_request_data('start', 'model', model_to_deploy))
        print('data sent to node: ', node.nodeName)
    except Exception as e:
        print('exception in node_manager.deploy_model', e)

def check_for_running(service_, service_type):
    if service_type == 'app':
        service_id = service_['appInstanceId']
    else:
        service_id = service_['model_id']

    response = post(SLCM_URL+'/service_lookup', json={
        "service_id" : service_id,
        "service_type" : service_type
    })

    if response.status_code == 200:
        return True
    return False


def deploy_models(models_to_deploy):
    for model_ in models_to_deploy:
        if not check_for_running(model_, 'model'):
            deploy_model(model_)


def deploy_app(app_to_deploy, all_data):
    if check_for_running(app_to_deploy, 'app'):
        print('app already running...')
        return
    try:
        node = find_appropriate_node(node_app)
        if not node:
            return
        send_using_kafka(node.nodeKafkaTopicName, build_request_data('start', 'app', app_to_deploy, all_data))
    except Exception as e:
        print('exception in node_manager.deploy_app', e)
