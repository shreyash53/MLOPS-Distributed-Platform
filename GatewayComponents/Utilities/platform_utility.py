import os
from re import S
import requests
import dotenv
dotenv.load_dotenv()


ns = os.getenv("num_sensors") # number of sensors
nm = os.getenv("num_models") # number of models

url = os.getenv('url')

sensors = dict()
sensor_ids_list = '<sensor_ids>'
for s_id in sensor_ids_list:
	sname = "S_"+str(s_id)
	sensors[sname] = os.getenv(sname) #

# models = dict()
# for x in range(1, int(nm)+1):
# 	Mname = "M_"+str(x)
# 	models[Mname] = os.getenv(Mname) #
	
	

def  getsensordata(sensor_id):
	sensor_id = "S_" + str(sensor_id)
	url_ = url + '/api' + '/sensor' + '/'+ sensors[sensor_id]
	response = requests.get(url_)
	# if response.status_code ==200:
	res = response.json()

	return res['data']
	# else:
	# 	return "error"
	
def getmodeldata(model_id,data):
	# model_id = "M_" + str(model_id)
	url_ = url + '/api' + '/model' + '/' + model_id
	response = requests.post(url_ , json = data)
	# if response.status_code ==200:
	res = response.json()
	return res['result']
	# else
	# 	return "error"
