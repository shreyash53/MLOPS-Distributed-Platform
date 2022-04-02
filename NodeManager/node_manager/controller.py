from json import loads
from time import sleep

from kafka import KafkaConsumer
from mongoengine.queryset.visitor import Q
from NodeManager.node_manager.deployment import deploy_app, deploy_models
from utilities.constants import kafka_url

from .model import NodeDocument


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
        if consumer_data['requesttype'] == 'start':
            deploy_models(consumer_data['models'])
            deploy_app(consumer_data['app'])
        else:
            terminate_models(consumer_data['models'])
            terminate_app(consumer_data['app'])

    except Exception as e:
        print('Error in node_manager.handle_deployment', e)
