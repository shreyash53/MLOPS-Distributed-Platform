from sensor_manager import app
if __name__ == "__main__":
	app.run(debug=True, threaded=True, port=9002,host='0.0.0.0')
