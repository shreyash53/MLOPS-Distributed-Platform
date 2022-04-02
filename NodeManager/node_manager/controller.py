from time import sleep
from .model import NodeDocument
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from utilities.constants import kafka_url, node_model, node_app

def send_using_kafka(topic_name, data):
    producer = KafkaProducer(bootstrap_servers=kafka_url,value_serializer=lambda x: 
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