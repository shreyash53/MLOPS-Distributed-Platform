from node_manager.controller import consumer_thread
from .service_restart import restart_model_consumer
from .load_balancer import min_load_balance
from threading import Thread
class DeploymentConsumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        consumer_thread()

class ServiceRestartConsumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        restart_model_consumer()


class consuming_load_balancing(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        min_load_balance()

