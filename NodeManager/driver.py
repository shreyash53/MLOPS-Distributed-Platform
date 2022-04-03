from node_manager import app
from utilities.constants import static_ip, static_port
from threading import Thread
if __name__ == '__main__':
    # kafka_consumer = Thread()
    app.run(debug=True, host=static_ip, port=static_port)