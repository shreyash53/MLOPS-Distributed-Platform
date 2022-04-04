from threading import Thread
from child_node.controller import consumer_thread
from child_node_app import app
from utilities.constants import static_ip, static_port
import sys
class KafkaConsumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        consumer_thread()

if __name__ == '__main__':
    kk = KafkaConsumer()
    kk.start()
    app.run(debug=True, host=static_ip, port=sys.argv[1])