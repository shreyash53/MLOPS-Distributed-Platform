from python_on_whales import docker
import threading
from BootstrapService.update_monitor_IP import *
from BootstrapService.dbconfig import *
import sys
import os
import dotenv
dotenv.load_dotenv()

monitor_ip = os.environ.get("monitoring_service_ip")
monitor_port = os.environ.get("monitoring_service_port")

db = mongodb()

class Build_run_service(threading.Thread):
    def __init__(self, 
                    dockerfile_destination_folder,
                    tag, host_port, 
                    service_name,
                    monitor_ip,
                    monitor_port,
                    entry_point_py_file_name):
        threading.Thread.__init__(self)
        self.dockerfile_destination_folder = dockerfile_destination_folder
        self.tag = tag
        self.host_port = host_port
        self.service_name = service_name
        self.monitor_ip = monitor_ip
        self.monitor_port = monitor_port
        self.entry_point_py_file_name = entry_point_py_file_name

    def run(self):
        create_docker_file(self.dockerfile_destination_folder,
                    monitor_ip=self.monitor_ip,
                    monitor_port=self.monitor_port,
                    entry_point_py_file_name=self.entry_point_py_file_name)
        docker_image = docker.build(self.dockerfile_destination_folder+'/', tags=self.tag)
        container = docker.run(self.tag, 
                            detach=True, 
                            publish=[(self.host_port, self.host_port)], 
                            networks='host')
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
    Build_run_service("./MonitoringService",
                      tag="monitor",
                      host_port=os.environ.get('monitoring_service_port'),
                      service_name=os.environ.get('monitoring_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                      entry_point_py_file_name="monitor.py").start()
 
    Build_run_service("./ServiceLifeCycleManager",
                      tag="service_life_cycle_manager",
                      host_port=os.getenv('SLCM_service_port'),
                      service_name=os.getenv('SLCM_service_name'),
                  # Build_run_service("./ServiceLifeCycleManager",
    #                   tag="service_life_cycle_manager",
    #                   host_port=os.getenv('SLCM_service_port'),
    #                   service_name=os.getenv('SLCM_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="ServiceLifecycleManager.py").start()

    # Build_run_service("./GatewayComponents",
    #                   tag="request_manager",
    #                   host_port=os.getenv('request_manager_service_port'),
    #                   service_name=os.getenv('request_manager_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="RequestManager.py").start()

    # Build_run_service("./LoggingService",
    #                   tag="logging",
    #                   host_port=os.getenv('logging_service_port'),
    #                   service_name=os.getenv('logging_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="logging_service.py").start()

    # Build_run_service("./Scheduler",
    #                   tag="scheduler",
    #                   host_port=os.getenv('scheduler_service_port'),
    #                   service_name=os.getenv('scheduler_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="scheduler.py").start()                      

    # Build_run_service("./NotificationManager",
    #                   tag="notification_manager",
    #                   host_port=os.getenv('notification_manager_service_port'),
    #                   service_name=os.getenv('notification_manager_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="notificationmanager.py").start()                      

    # Build_run_service("./SensorManager",
    #                   tag="sensor_manager",
    #                   host_port=os.getenv('sensor_manager_service_port'),
    #                   service_name=os.getenv('sensor_manager_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="Sensor_Manager_Driver.py").start()

    # Build_run_service("./Deployer",
    #                   tag="deployer",
    #                   host_port=os.getenv('deployer_service_port'),
    #                   service_name=os.getenv('deployer_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="app_model_deploy.py").start()                      

    # Build_run_service("./NodeManager",
    #                   tag="node_manager",
    #                   host_port=os.getenv('node_manager_service_port'),
    #                   service_name=os.getenv('node_manager_service_name'),
    #                   monitor_ip=monitor_ip,
    #                   monitor_port=monitor_port,
    #                 entry_point_py_file_name="driver.py").start()
        monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="ServiceLifecycleManager.py").start()

    Build_run_service("./GatewayComponents",
                      tag="request_manager",
                      host_port=os.getenv('request_manager_service_port'),
                      service_name=os.getenv('request_manager_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="RequestManager.py").start()

    Build_run_service("./LoggingService",
                      tag="logging",
                      host_port=os.getenv('logging_service_port'),
                      service_name=os.getenv('logging_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="logging_service.py").start()

    Build_run_service("./Scheduler",
                      tag="scheduler",
                      host_port=os.getenv('scheduler_service_port'),
                      service_name=os.getenv('scheduler_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="scheduler.py").start()                      

    Build_run_service("./NotificationManager",
                      tag="notification_manager",
                      host_port=os.getenv('notification_manager_service_port'),
                      service_name=os.getenv('notification_manager_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="notificationmanager.py").start()                      

    Build_run_service("./SensorManager",
                      tag="sensor_manager",
                      host_port=os.getenv('sensor_manager_service_port'),
                      service_name=os.getenv('sensor_manager_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="Sensor_Manager_Driver.py").start()

    Build_run_service("./Deployer",
                      tag="deployer",
                      host_port=os.getenv('deployer_service_port'),
                      service_name=os.getenv('deployer_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="app_model_deploy.py").start()                      

    Build_run_service("./NodeManager",
                      tag="node_manager",
                      host_port=os.getenv('node_manager_service_port'),
                      service_name=os.getenv('node_manager_service_name'),
                      monitor_ip=monitor_ip,
                      monitor_port=monitor_port,
                    entry_point_py_file_name="driver.py").start()




# 192.168.21.240


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
