from python_on_whales import docker
from BootstrapService.update_monitor_IP import *
from BootstrapService.dbconfig import *
import os
import dotenv
dotenv.load_dotenv()

if __name__ == "__main__":
    db = mongodb()

    monitor_ip = os.environ.get("monitoring_service_ip")
    dockerfile_destination_folder = "./ChildNode"
    tag = "child_node"
    host_port = os.getenv("child_node_service_port")
    service_name = os.getenv("child_node_service_name")
    entry_point_py_file_name = "driver.py"

    create_docker_file(dockerfile_destination_folder,
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name=entry_point_py_file_name)
    docker_image = docker.build(dockerfile_destination_folder+'/', tags=tag)
    container = docker.run(tag, 
                        detach=True, 
                        volumes=[("/var/run/docker.sock","/var/run/docker.sock")],
                        publish=[(host_port, 5000)])
    new_service = Bootstrap(service_name=service_name,
                            contrainer_id=str(container))

    new_service.save()