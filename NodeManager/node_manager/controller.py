from time import sleep
from .model import NodeDocument
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from utilities.constants import kafka_url, node_model, node_app
from mongoengine.queryset.visitor import Q


def node_validated(node_data):
    if (node_data['nodePort'] and node_data['nodeIp'] and (not NodeDocument.objects.filter(Q(nodePort=node_data['nodePort']) & Q(nodeIP=node_data['nodeIp'])))) \
        or (node_data['nodeUrl'] and (not NodeDocument.objects.filter(Q(nodeUrl=node_data['NodeUrl'])))):
        return True
    return False


def add_node(node_data):
    try:
        if not node_validated(node_data):
            node_ = NodeDocument(**node_data)
            node_.save()
    except Exception as e:
        print('error while adding node in node_manager.add_node', e)


def add_all_nodes(nodes_data):
    for node_data in nodes_data:
        add_node(node_data)
    return "Added Valid Nodes"


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
        send_using_kafka(node.nodeKafkaTopicName, model_to_deploy)
        print('data sent to node: ', node.nodeName)
    except Exception as e:
        print('exception in node_manager.deploy_model', e)


def deploy_models(models_to_deploy):
    for model_ in models_to_deploy:
        deploy_model(model_)


def deploy_app(app_to_deploy):
    try:
        node = find_appropriate_node(node_app)
        if not node:
            return
        send_using_kafka(node.nodeKafkaTopicName, app_to_deploy)
    except Exception as e:
        print('exception in node_manager.deploy_app', e)


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
        deploy_models(consumer_data['models'])
        deploy_app(consumer_data['app'])
    except Exception as e:
        print('Error in node_manager.handle_deployment', e)
