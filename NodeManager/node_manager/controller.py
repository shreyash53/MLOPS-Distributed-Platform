from json import loads, dumps
from time import sleep
import traceback
from flask import jsonify

from kafka import KafkaConsumer
from mongoengine.queryset.visitor import Q
from node_manager.deployment import deploy_app, deploy_models
from utilities.constants import HTTP_OK_STATUS_CODE, kafka_url
from node_manager.terminate import terminate_app, terminate_all_models
from .model import NodeDocument


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

def get_node_by_id(id):
    try:
        return NodeDocument.objects(id = id).get()
    except Exception as e:
        print('failed to retrieve', e)

def add_all_nodes(nodes_data):
    # print(nodes_data)
    # print(type(nodes_data))
    for node_data in nodes_data:
        add_node(node_data)
    return "Added Valid Nodes"


def consumer_logic(consumer_data):
    consumer_data = consumer_data.value
    print('data: ', consumer_data)
    if consumer_data['request_type'] == 'start':
        deploy_models(consumer_data['models'])
        deploy_app(consumer_data['app'], consumer_data)
    else:
        terminate_all_models(consumer_data['models'])
        terminate_app(consumer_data['app'])

def consumer_thread():
    while True:
        try:
            consumer = KafkaConsumer(
                'app_deploy2',
                bootstrap_servers=[kafka_url],
                auto_offset_reset='earliest',
                enable_auto_commit=True, 
                group_id='my-group-2',
                value_deserializer=lambda x: loads(x.decode('utf-8'))
            )
            print('inside nodemanager consumer thread')
            for data in consumer:
                consumer_logic(data)


        except Exception as e:
            print(traceback.format_exc())
            print('Error in node_manager.consumer_thread', e)


def get_node_list():
    try:
        node_list = [
            node.nodeName for node in NodeDocument.objects()
        ]
        return jsonify(*node_list), HTTP_OK_STATUS_CODE
    except Exception as e:
        print('error in node_manager.get_node_list', e)
        return

def get_node_performance_data():
    try:
        stats = [
            node.get_usage() for node in NodeDocument.objects()
        ]
        return dumps(stats), HTTP_OK_STATUS_CODE
    except Exception as e:
        print('error in node_manager.get_node_performance_data', e)
        return 