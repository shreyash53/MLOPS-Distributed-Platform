from NodeManager.node_manager.model import RunningServices
from mongoengine.queryset.visitor import Q
from .deployment import send_using_kafka, build_request_data

def find_node_with_service(service_type, service_id):
    service_ = RunningServices.objects.filter(Q(serviceType = service_type) & Q(serviceId = service_id))
    if service_:
        return service_.first().node


def terminate_model(model):
    try:
        node = find_node_with_service('model', model['model_id'])
        if not node:
            print('no running model found with id: ', model['model_id'])
            return 
        send_using_kafka(node.nodeKafkaTopicName, build_request_data('stop', 'model', model))
    except Exception as e:
        print('error while terminating model in node_manager.terminate_model')

def terminate_all_models(models_to_terminate):
    for model in models_to_terminate:
        terminate_model(model)

def terminate_app(app):
    try:
        node = find_node_with_service('app', app['appInstanceId'])
        if not node:
            print('no running app found with id', app['appInstanceId'])
            return 
        send_using_kafka(node.nodeKafkaTopicName, build_request_data('stop', 'app', app))
    except Exception as e:
        print('error while terminating app in node_manager.terminate_app')