from sensor_manager import *
import os
from dotenv import load_dotenv
import threading

load_dotenv()

PORT = os.getenv('sensor_manager_service_port')

t1 = threading.Thread(target=Start_Services)
t1.start()

if __name__ == "__main__":
	# app.run(debug=True, threaded=True, port=SENSOR_MGR_PORT, host='0.0.0.0')
	print("HEHEHE")
	send_log("INFO", "Hi this is Sensor Manager")
	# print("HEHEHE")
	app.run(debug=False, threaded=True, port=PORT, host='0.0.0.0')
