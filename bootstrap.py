from python_on_whales import docker
import threading
from BootstrapService.update_monitor_IP import *
from BootstrapService.dbconfig import *
import sys
import os
import dotenv
dotenv.load_dotenv()

db = mongodb()

class Build_run_service(threading.Thread):
    def __init__(self, docker_file_path, tag, host_port, service_name):
        threading.Thread.__init__(self)
        self.docker_file_path = docker_file_path
        self.tag = tag
        self.host_port = host_port
        self.service_name = service_name

    def run(self):
        docker_image = docker.build(self.docker_file_path, tags=self.tag)
        container = docker.run(self.tag, detach=True, 
                            publish=[(self.host_port, 5000)])
        new_service = Bootstrap(service_name=self.service_name,
                                contrainer_id=str(container))

        new_service.save()


def stop_service(service_name):
    container = Bootstrap.objects(service_name=service_name)
    if container.count() == 0:
        print("container_id not present for ", service_name)
        return
    container = container.first()
    try:
        docker.stop(container.service_name)
    except Exception as e:
        print(e)
    container.delete()
    return "ok"


if __name__ == "__main__":
    monitor_ip = sys.argv[1]
    create_docker_file("./MonitoringService",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="monitor.py")
    Build_run_service("./MonitoringService/",
                      tag="monitor",
                      host_port=os.getenv('monitoring_service_port'),
                      service_name=os.getenv('monitoring_service_name')).start()
    create_docker_file("./ServiceLifeCycleManager",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="ServiceLifeCycleManager.py")
    Build_run_service("./ServiceLifeCycleManager/",
                      tag="service_life_cycle_manager",
                      host_port=os.getenv('SLCM_service_port'),
                      service_name=os.getenv('SLCM_service_name')).start()
    create_docker_file("./GatewayComponents",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="RequestManager.py")
    Build_run_service("./GatewayComponents/",
                      tag="request_manager",
                      host_port=os.getenv('request_manager_service_port'),
                      service_name=os.getenv('request_manager_service_name')).start()
    create_docker_file("./LogginService",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="logging_service.py")
    Build_run_service("./LogginService/",
                      tag="logging",
                      host_port=os.getenv('logging_service_port'),
                      service_name=os.getenv('logging_service_name')).start()
    create_docker_file("./Scheduler",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="scheduler.py")
    Build_run_service("./Scheduler/",
                      tag="scheduler",
                      host_port=os.getenv('scheduler_service_port'),
                      service_name=os.getenv('scheduler_service_name')).start()                      
    create_docker_file("./NotificationManager",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="notificationmanager.py")
    Build_run_service("./NotificationManager/",
                      tag="notification_manager",
                      host_port=os.getenv('notification_manager_service_port'),
                      service_name=os.getenv('notification_manager_service_name')).start()                      
    create_docker_file("./SensorManager",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="Sensor_Manager_Driver.py")
    Build_run_service("./SensorManager/",
                      tag="sensor_manager",
                      host_port=os.getenv('sensor_manager_service_port'),
                      service_name=os.getenv('sensor_manager_service_name')).start()
    create_docker_file("./Deployer",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="app_model_deploy.py")
    Build_run_service("./Deployer/",
                      tag="deployer",
                      host_port=os.getenv('deployer_service_port'),
                      service_name=os.getenv('deployer_service_name')).start()                      
    create_docker_file("./NodeManager",
                    monitor_ip=monitor_ip,
                    entry_point_py_file_name="driver.py")
    Build_run_service("./NodeManager/",
                      tag="node_manager",
                      host_port=os.getenv('node_manager_service_port'),
                      service_name=os.getenv('node_manager_service_name')).start()







# import subprocess   
# import time


# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "./MonitoringService/monitor.py"], stdout=subprocess.PIPE)

# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "./ServiceLifecycleManager/ServiceLifecycleManager.py"],
#                  stdout=subprocess.PIPE)

# time.sleep(1)

# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "./ChildNode/driver.py"], stdout=subprocess.PIPE)
# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "./GatewayComponents/RequestManager.py"], stdout=subprocess.PIPE)
# # subprocess.Popen(['gnome-terminal', '--', "python",
# #                  "./LogginService/logging_service.py"], stdout=subprocess.PIPE)
# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "./Scheduler/scheduler.py"], stdout=subprocess.PIPE)
# # subprocess.Popen(['gnome-terminal', '--', "python",
# #                  "NotificationManager/notificationmanager.py"], stdout=subprocess.PIPE)
# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "./SensorManager/Sensor_Manager_Driver.py"], stdout=subprocess.PIPE)

# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "Deployer/app_model_deploy.py"], stdout=subprocess.PIPE)
# subprocess.Popen(['gnome-terminal', '--', "python",
#                  "NodeManager/driver.py"], stdout=subprocess.PIPE)
