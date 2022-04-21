from python_on_whales import docker
from BootstrapService.update_monitor_IP import *
from BootstrapService.dbconfig import *
import os
import dotenv
dotenv.load_dotenv()
import sys


if __name__ == "__main__":
    SERVICE_PORT = sys.argv[1]
    NODE_ID = sys.argv[2]
    db = mongodb()
    
    monitor_ip = os.environ.get("monitoring_service_ip")
    monitor_port = os.getenv('monitoring_service_port')
    dockerfile_destination_folder = "./ChildNode"
    tag = "child_node"
    host_port = os.getenv("child_node_service_port")
    service_name = os.getenv("child_node_service_name")
    entry_point_py_file_name = "driver.py"
    
    create_docker_file(dockerfile_destination_folder,
                monitor_ip=monitor_ip,
                monitor_port=monitor_port,
                entry_point_py_file_name=entry_point_py_file_name,
                for_child_node=True)

    docker_image = docker.build(dockerfile_destination_folder+'/', tags=tag)
    container = docker.run(tag, 
                        detach=True, 
                        envs={"SERVICE_PORT":SERVICE_PORT,
                                "NODE_ID":NODE_ID},
                        volumes=[("/var/run/docker.sock","/var/run/docker.sock")],
                        networks='host',
                        publish=[(host_port, host_port)])
    new_service = Bootstrap(service_name=service_name,
                            contrainer_id=str(container))

    new_service.save()