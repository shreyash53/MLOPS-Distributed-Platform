from sqlalchemy import false
from utilities.constants import HTTP_OK_STATUS_CODE, SLCM_URL
from node_manager.model import RunningServices
from mongoengine.queryset.visitor import Q
from .deployment import send_using_kafka, build_request_data
from requests import post
from .model import NodeDocument


def find_node_with_service(service_type, service_id):
    # service_ = RunningServices.objects.filter(Q(serviceType = service_type) & Q(serviceId = service_id))
    # if service_:
    #     return service_.first().node
    response = post(SLCM_URL+'/service_lookup', json={
        "service_id" : service_id,
        "service_type" : service_type
    })
    if response.status_code != 200:
        print('service not running')
    response = response.json()
    node_ = NodeDocument.objects.filter(nodeName = response['node'])
    if not node_:
        print('node not found with id', response['node'])
        return
    print(f"node {node_.first().nodeName} found with id {response['node']}")
    return node_.first()

def terminate_model(model):
    try:
        node = find_node_with_service('model', model['model_id'])
        if not node:
            print('no running model found with id: ', model['model_id'])
            return 
        send_using_kafka(node.nodeKafkaTopicName, build_request_data('stop', 'model', model))
    except Exception as e:
        print('error while terminating model in node_manager.terminate_model',e)

def check_to_stop_model(model):
    try:
        res = post(SLCM_URL+'/change_count', json={
            "service_id" : model['model_id'],
            "type" : "decrement"
        })
        if res.status_code != HTTP_OK_STATUS_CODE:
            print('Did not get proper response from slcm for decrement of model usage')
            return False
        if res.json()['result'] == 0:
            return True
        return False
    except Exception as e:
        print('error in node_manager.check_to_stop_model', e)
        return False

def terminate_all_models(models_to_terminate):
    for model in models_to_terminate:
        if check_to_stop_model(model):
            terminate_model(model)

def terminate_app(app):
    try:
        node = find_node_with_service('app', app['appInstanceId'])
        if not node:
            print('no running app found with id', app['appInstanceId'])
            return 
        print('running app found with id', app['appInstanceId'])
        send_using_kafka(node.nodeKafkaTopicName, build_request_data('stop', 'app', app))
    except Exception as e:
        print('error while terminating app in node_manager.terminate_app',e)