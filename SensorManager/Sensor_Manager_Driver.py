from sensor_manager import app
import os
from dotenv import load_dotenv

load_dotenv()

SENSOR_MGR_PORT = os.getenv('SENSOR_MGR_PORT')

if __name__ == "__main__":
	# app.run(debug=True, threaded=True, port=SENSOR_MGR_PORT, host='0.0.0.0')
	app.run(debug=True, threaded=True, port=9003, host='0.0.0.0')
