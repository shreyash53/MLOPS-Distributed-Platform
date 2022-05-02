from python_on_whales import docker
from python_on_whales.exceptions import NoSuchImage
from child_node.model import ServicesRunning
from child_node_config import NODE_ID
from utilities.azure_config import download_dir

import os
from time import sleep
import zipfile
from json import dumps
import urllib.request

from kafka import KafkaProducer
from utilities.constants import APP_DIR, MODEL_DIR, SLCM_TOPIC_NAME, CHILD_NODE_URL, kafka_url
import traceback
from utilities.helper import edit_docker_file
from utilities.constants import MONITOR_IP, MONITOR_PORT
file_stub = '{}/{}'

APP_PORT_SERVICE = 11000
MODEL_PORT_SERVICE = 12000
MY_IP = urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')

def send_using_kafka(topic_name, data):
    producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    producer.send(topic_name, data)
    # sleep(2)


def make_and_move_in_directory(service_type, service_name):
    print('file stub', file_stub)
    if service_type == 'app':
        file_loc = file_stub.format(APP_DIR, service_name)
    else:
        file_loc = file_stub.format(MODEL_DIR, service_name)

    file_loc += '/'
    print('file_loc - inside', file_loc)
    try:
        os.listdir(file_loc)
        return file_loc, True
    except Exception as e:
        os.makedirs(file_loc), False
     


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
    try:
        print('now downloading file....')
        service_name = get_service_name(service_type, service_details)
        print('service_name', service_name)
        service_location = get_service_location(service_type, service_details)
        print('service_location', service_location)
        file_loc, dir_exists = make_and_move_in_directory(service_type, service_name)
        print('file_loc', file_loc)
        if(dir_exists):
            print('dir already exists')
            return file_loc
        file_name = os.path.basename(service_location)
        print('file_name', file_name)
        service_address = file_loc + service_name + '.zip'
        print('service_address', service_address)
        download_dir(service_location, file_name, service_address)
        extract_file(service_address)

        return file_loc
    except Exception as e:
        print('error while downloading files', e)

def extract_file(file_loc):
    try:
        with zipfile.ZipFile(file_loc, "r") as zip_ref:
            Path_out = os.path.dirname(file_loc)
            zip_ref.extractall(Path_out)
            # print("yes..line 50")
    except Exception as e:
        print('error while extracting files', e)


def make_dockerignore(file_loc):
    with open(file_loc + '/.dockerignore', 'w') as file:
        file.write('*.zip')

def register_service_in_node(service_type, data, file_loc, tag_name, container_id, port):
    print(data)
    try:
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
    except Exception as e:
        print(traceback.format_exc())
        print('error while registering service in node', e)


def register_service_with_slcm(service_type, data, service_ip, service_port):
    request_ = {
        "instance_id" : get_service_id(service_type, data),
        "service_name" : get_service_name(service_type, data),
        "service_type" : service_type,
        "request_type" : "register",
        "service_ip" : service_ip,
        "service_port": service_port,
        "node" : NODE_ID
    }
    send_using_kafka(SLCM_TOPIC_NAME, request_)

def get_env_data(data, service_type, port):
    try:
        d = {
            "SERVICE_PORT" : port
        }
        if service_type != 'app':
            print('service_type: ',service_type)
            return d
        num_models = len(data['models_data'])
        num_sensors = len(data['sensor_data'])
        result = {
            "num_models" : num_models,
            "num_sensors" : num_sensors,
            **d
        }
        # for data_ in data['models_data']:
            # result[data_['model_id']] = data_['model_id']
            # result['M_{}'.format(data_['model_id'])] = data_['model_id']

        for data in data['sensor_data']:
            result['S_{}'.format(data['sensor_app_id'])] = data['sensor_binding_id']
        
        result['url'] = CHILD_NODE_URL
        print('all env variables')
        print(result)
        return result
    except Exception as e:
        print(data)
        print(traceback.format_exc())
        print('error while getting env data', e)

def image_not_available(tag_name):
    try:
        docker.image.inspect(tag_name)
        return False
    except NoSuchImage:
        print('Image not available')
    except Exception as e:
        print('error in image_not_available', e)
    return True

def deployment_handler(service_type, data):
    global MODEL_PORT_SERVICE, APP_PORT_SERVICE
    try:

        if service_type == 'app':
            data_ = data['app_data']
            # dir_ = APP_DIR
        else:
            data_ = data
            # dir_ = MODEL_DIR
        file_loc = download_files(service_type, data_)
        if not file_loc:
            print('In deployment handler of child node, couldn\'t download files')
            return
        # file_loc, service_address = flag

        # extract_file(service_address)
        edit_docker_file(file_loc, get_service_id(service_type, data_), service_type, MONITOR_IP, MONITOR_PORT)
        make_dockerignore(file_loc)
        tag_name = get_service_name(service_type, data_)
        if image_not_available(tag_name):
            docker_image = docker.build(file_loc, tags=tag_name)
        if service_type == 'app':
            container = docker.run(tag_name, detach=True, publish=[(APP_PORT_SERVICE, APP_PORT_SERVICE)], envs=get_env_data(data, service_type, APP_PORT_SERVICE), networks='host')
        else:
            container = docker.run(tag_name, detach=True, publish=[(MODEL_PORT_SERVICE, MODEL_PORT_SERVICE)], envs=get_env_data(data, service_type, MODEL_PORT_SERVICE), networks='host')
        
        if not container:
            print('not able to run container')
            return 
        #store docker details
        if service_type == 'app':
            port = APP_PORT_SERVICE
            APP_PORT_SERVICE += 1
        else:
            port = MODEL_PORT_SERVICE
            MODEL_PORT_SERVICE += 1
        register_service_in_node(service_type, data_, file_loc, tag_name, str(container), str(port))
        register_service_with_slcm(service_type, data_, MY_IP, str(port))
    except Exception as e:
        print('error while deployment handling', e)

