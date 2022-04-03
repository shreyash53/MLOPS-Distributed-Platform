from python_on_whales import docker
from child_node.model import ServicesRunning
from child_node_config import NODE_ID
from utilities.azure_config import download_dir

import os
from time import sleep
import zipfile
from json import dumps

from kafka import KafkaProducer
from utilities.constants import APP_DIR, MODEL_DIR, SLCM_TOPIC_NAME, CHILD_NODE_URL

file_stub = '{}/{}'

PORT_SERVICE = 11000

def send_using_kafka(topic_name, data):
    producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    producer.send(topic_name, data)
    sleep(2)


def make_and_move_in_directory(service_type, service_name):
    if service_type == 'app':
        file_loc = file_stub.format(APP_DIR, service_name)
    else:
        file_loc = file_stub.format(MODEL_DIR, service_name)
    try:
        os.listdir(file_loc)
    except Exception as e:
        os.makedirs(file_loc)
    return file_loc


def get_service_name(service_type, service_details):
    if service_type == 'app':
        return service_details['appName']
    else:
        return service_details['model_name']

def get_service_id(service_type, service_details):
    if service_type == 'app':
        return service_details['appInstanceId']
    else:
        return service_details['model_id']


def get_service_location(service_type, service_details):
    if service_type == 'app':
        return service_details['appLoc']
    else:
        return service_details['model_location']


def download_files(service_type, service_details):
    service_name = get_service_name(service_type, service_details)
    service_location = get_service_location(service_type, service_details)
    file_loc = make_and_move_in_directory(
        service_type, service_details[service_name])
    file_name = os.path.basename(service_location)
    service_address = file_loc + service_name + '.zip'
    download_dir(service_location, file_name, service_address)
    return file_loc, service_address


def extract_file(file_loc):
    with zipfile.ZipFile(file_loc, "r") as zip_ref:
        Path_out = os.path.dirname(file_loc)
        zip_ref.extractall(Path_out)
        # print("yes..line 50")


def make_dockerignore(file_loc):
    with open(file_loc + '/.gitignore', 'w') as file:
        file.write('*.zip')

def register_service_in_node(service_type, data, file_loc, tag_name, container_id, port):
    service_ = ServicesRunning(
        serviceId = get_service_id(service_type, data),
        serviceName = get_service_name(service_type, data),
        serviceType = service_type,
        serviceDockerTagName = tag_name,
        serviceDockerContainerName = container_id,
        serviceDockerFileLocation = file_loc,
        serviceNodeId = NODE_ID,
        serviceDockerPort = port
    )
    service_.save()

def register_service_with_slcm(service_type, data):
    request_ = {
        "instance_id" : get_service_id(service_type, data),
        "service_name" : get_service_name(service_type, data),
        "service_type" : service_type,
        "request_type" : "start"
    }
    send_using_kafka(SLCM_TOPIC_NAME, request_)

def get_env_data(data):
    num_models = len(data['model'])
    num_sensors = len(data['sensor'])
    result = {
        "num_models" : num_models,
        "num_sensors" : num_sensors
    }
    for data in data['model']:
        result['M_{}'.format(data['model_id'])] = data['model_id']

    for data in data['sensor']:
        result['S_{}'.format(data['sensor_app_id'])] = data['sensor_binding_id']
    
    result['url'] = CHILD_NODE_URL
    return result

def deployment_handler(service_type, data):
    file_loc, service_address = download_files(service_type, data['app'])
    extract_file(service_address)
    make_dockerignore(file_loc)
    tag_name = get_service_name(service_type, data['app'])
    docker_image = docker.build(file_loc, tags=tag_name)
    if service_type == 'app':
        container = docker.run(tag_name, detach=True, publish=[(PORT_SERVICE, 8008)], envs=get_env_data(data))
    else:
        container = docker.run(tag_name, detach=True, publish=[(PORT_SERVICE, 8008)])
    if not container:
        print('not able to run container')
        return 
    #store docker details
    register_service_in_node(service_type, data['app'], file_loc, tag_name, str(container), str(PORT_SERVICE))
    register_service_with_slcm(service_type, data['app'])

