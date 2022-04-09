from sensor_manager import *
import os
from dotenv import load_dotenv
import threading

load_dotenv()

SENSOR_MGR_PORT = os.getenv('SENSOR_MGR_PORT')

t1 = threading.Thread(target=Start_Services)
t1.start()

if __name__ == "__main__":
	# app.run(debug=True, threaded=True, port=SENSOR_MGR_PORT, host='0.0.0.0')
	app.run(debug=False, port="5000", host='0.0.0.0')
