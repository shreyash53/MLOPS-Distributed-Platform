from node_manager import app
from utilities.constants import static_ip, static_port

if __name__ == '__main__':
    app.run(debug=True, host=static_ip, port=static_port)