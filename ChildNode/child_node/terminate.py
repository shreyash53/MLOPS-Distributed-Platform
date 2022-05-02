
from webbrowser import get
from utilities.constants import SLCM_TOPIC_NAME
from .child_node_config import NODE_ID
from child_node.model import ServicesRunning
from .deployment import get_service_id, get_service_location, get_service_name, send_using_kafka
from mongoengine.queryset.visitor import Q
from python_on_whales import docker 

def terminate_service(service_):
    try:
        docker.stop(service_.serviceDockerContainerName)
    except Exception as e:
        print('error in terminate_service', e)
    

def unregister_service_with_slcm(service_type, data):
    request_ = {
        "instance_id" : get_service_id(service_type, data),
        "service_name" : get_service_name(service_type, data),
        "service_type" : service_type,
        "request_type" : "stopped"
    }
    send_using_kafka(SLCM_TOPIC_NAME, request_)

def termination_handler(service_type, data):
    try:
        service_ = ServicesRunning.objects.filter(
            Q(serviceType = service_type) &
            Q(serviceId = get_service_id(service_type, data)) &
            Q(serviceNodeId = NODE_ID)
        )

        if not service_:
            print('No service found for termination with service id', get_service_id(service_type, data))
            return
        
        service_ = service_.first()

        terminate_service(service_)
        unregister_service_with_slcm(service_type, data)
        service_.delete()
        
    except Exception as e:
        print('error occurred during childnode.termination_handler', e)
