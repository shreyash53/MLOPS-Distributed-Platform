from node_manager.controller import consumer_thread
from node_manager_app import app
from utilities.constants import static_ip, static_port
from threading import Thread
class KafkaConsumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        consumer_thread()

if __name__ == '__main__':
    kk = KafkaConsumer()
    kk.start()
    app.run(debug=False, host=static_ip, port=static_port)