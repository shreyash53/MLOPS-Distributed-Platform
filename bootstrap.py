from python_on_whales import docker
docker_image = docker.build('.', tags="test_img:1.1")
redis_container = docker.run("test_img:1.1", detach=True, publish=[(6370, 8001)])





docker.stop(redis_container)







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
