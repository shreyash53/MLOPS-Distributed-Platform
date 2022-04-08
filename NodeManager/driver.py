from node_manager_app import app
from utilities.constants import static_ip, static_port
from node_manager.consumers import DeploymentConsumer, ServiceRestartConsumer

if __name__ == '__main__':
    kk = DeploymentConsumer()
    kk.start()
    srvc = ServiceRestartConsumer()
    srvc.start()
    app.run(debug=False, host=static_ip, port=static_port)