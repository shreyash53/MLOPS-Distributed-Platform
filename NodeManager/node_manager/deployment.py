from json import dumps
from time import sleep, time_ns
from NodeManager.utilities.log_generator import send_log

from node_manager.model import NodeDocument
from utilities.constants import HTTP_OK_STATUS_CODE, kafka_url, node_app, node_model, SLCM_URL
from kafka import KafkaProducer
from requests import post
from .vm_manager import *
from mongoengine.queryset.visitor import Q


def build_request_data(request_type, service_type, data, all_data=None):
    if service_type == "app":
        return {
            "requesttype": request_type,
            "servicetype": service_type,
            "data": {
                "app_data": data,
                "sensor_data": all_data["sensors"],
                "models_data": all_data["models"],
            },
        }
    return {"requesttype": request_type, "servicetype": service_type, "data": data}


def send_using_kafka(topic_name, data):
    producer = KafkaProducer(
        bootstrap_servers=kafka_url, value_serializer=lambda x: dumps(
            x).encode("utf-8")
    )
    producer.send(topic_name, data)
    # sleep(2)


def node_validated(node_data):
    if (node_data['nodePortNo'] and node_data['nodeIpAddress'] and (not NodeDocument.objects.filter(Q(nodePortNo=node_data['nodePortNo']) & Q(nodeIpAddress=node_data['nodeIpAddress'])))) \
            or (node_data['nodeUrl'] and (not NodeDocument.objects.filter(Q(nodeUrl=node_data['NodeUrl'])))):
        return True
    return False


def add_node(node_data):
    try:
        if node_validated(node_data):
            node_ = NodeDocument(**node_data)
            node_.save()
    except Exception as e:
        print('error while adding node in node_manager.add_node', e)


def start_new_node(node_type):
    print("start new node type:", node_type)
    suffix = str(time_ns())
    node_name = suffix
    node_ip = createVM(node_name)
    if node_ip is None:
        print("Failed to create new node!")
        return None
    else:
        node_data = {
            "nodeName": node_name,
            "nodeIpAddress": node_ip,
            "nodePortNo": 5000,
            "nodeUrl": f'{node_ip}:{5000}',
            "nodeType": node_type,  # platform, node_app, node_model
        }

        add_node(node_data)


def find_appropriate_node(node_type):
    nodes = NodeDocument.objects.filter(
        nodeType=node_type).order_by("node_cpu_usage", "node_ram_usage")
    if not nodes:
        print("No nodes available, adding some nodes of type", node_type)
        start_new_node(node_type)
        return
    node = nodes.first()
    if node.node_cpu_usage > 70 and node.node_ram_usage > 65:
        # send request to start node of same type
        print("High load on existing machines, adding a new node of type", node_type)
        start_new_node(node_type)

    return node


def deploy_model(model_to_deploy):
    try:
        node = find_appropriate_node(node_model)
        if not node:
            return

        send_using_kafka(
            node.nodeKafkaTopicName,
            build_request_data("start", "model", model_to_deploy),
        )
        print("data sent to node: ", node.nodeName)
    except Exception as e:
        send_log("ERR", "ERROR in node_manager.deploy_model, " + str(e))
        print("exception in node_manager.deploy_model", e)


def check_for_running(service_, service_type):
    if service_type == "app":
        service_id = service_["appInstanceId"]
    else:
        service_id = service_["model_id"]

    response = post(
        SLCM_URL + "/service_lookup",
        json={"service_id": service_id, "service_type": service_type},
    )

    if response.status_code == HTTP_OK_STATUS_CODE:
        res = post(SLCM_URL+'/change_count', json={
            "service_id" : service_id,
            "type" : "increment"
        })
        if res.status_code != HTTP_OK_STATUS_CODE:
            print('Did not get proper response from slcm for increment of model usage')
        return True
    return False


def deploy_models(models_to_deploy):
    for model_ in models_to_deploy:
        if not check_for_running(model_, "model"):
            deploy_model(model_)


def deploy_app(app_to_deploy, all_data):
    if check_for_running(app_to_deploy, "app"):
        print("app already running...")
        return
    try:
        node = find_appropriate_node(node_app)
        if not node:
            return
        send_using_kafka(
            node.nodeKafkaTopicName,
            build_request_data("start", "app", app_to_deploy, all_data),
        )
    except Exception as e:
        send_log("ERR", "ERROR in node_manager.deploy_app, " + str(e))
        print("exception in node_manager.deploy_app", e)
