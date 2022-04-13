from threading import Thread
from child_node.controller import consumer_thread
from child_node.load_balancer import sending_load
from child_node_app import app
from utilities.constants import static_ip, static_port
import sys
class KafkaConsumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        consumer_thread()

class uploading_load_balancing(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        sending_load()

if __name__ == '__main__':
    kk = KafkaConsumer()
    kk.start()
    load=uploading_load_balancing()
    load.start()
    # app.run(debug=False, host=static_ip, port=sys.argv[1])
    app.run(debug=False, host=static_ip, port=sys.argv[1])