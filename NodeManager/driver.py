from node_manager_app import app
from utilities.constants import static_ip, static_port
from node_manager.consumers import DeploymentConsumer, ServiceRestartConsumer,consuming_load_balancing

if __name__ == '__main__':
    kk = DeploymentConsumer()
    kk.start()
    srvc = ServiceRestartConsumer()
    srvc.start()
    load=consuming_load_balancing()
    load.start()
    app.run(debug=False, host=static_ip, port=static_port)