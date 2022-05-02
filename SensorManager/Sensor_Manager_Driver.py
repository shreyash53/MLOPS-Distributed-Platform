from sensor_manager import *
import os
from dotenv import load_dotenv
import threading

load_dotenv('../.env')

PORT = os.getenv('sensor_manager_service_port')

t1 = threading.Thread(target=Start_Services)
t1.start()

if __name__ == "__main__":
	# app.run(debug=True, threaded=True, port=SENSOR_MGR_PORT, host='0.0.0.0')
	app.run(debug=False, threaded=True, port=PORT, host='0.0.0.0')
