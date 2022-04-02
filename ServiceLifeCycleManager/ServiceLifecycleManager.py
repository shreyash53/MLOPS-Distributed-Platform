from flask import Flask, request
import service_utilities as sv
import kafka
from json import loads
import threading
import dotenv
import os
dotenv.load_dotenv()

app = Flask(__name__)

PORT = os.getenv("PORT")
def consume():
	consumer = kafka.KafkaConsumer(
    'register',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

	for message in consumer:
		data = message.value
		instance = data["instance_id"]
		if data["request_type"] == "register":
			data["state"] = "running"
			sv.savetodb(data)
		elif data["request_type"] == "unregister":
			sv.updatedb({"instance_id"  : data["instance_id"]} , {"state" :"stopped" })


''''
# expected request from node manager when docker service is started  
@app.route("/register", methods=["POST"])
def service_start():
	data = request.get_json()
	if data["type"] == "application":
		models = data["models"]
		for x in models:
			sv.inc_service(x.name , x.type)

	return sv.savetodb(data)

# when a serivce is stopped voluntarily
@app.route("/service_stop",methods =["POST"])
def service_stop():
	data = request.get_json()
	#need to notify monitoring service
	return sv.updatedb({"instance_id"  : data["instance_id"]} , {"state" :"killed" })
'''

#hit by service to get port of another service
@app.route("/service_lookup", methods=["POST"])
def service_lookup():
	request_data = request.get_json()
	ser=request_data["service_name"]
	obj = sv.fetchdb({"service_name" :ser })[0]
	print(obj.to_json(),"dsfsddsfdsfsd")
	if(obj!=None and obj["state"] == "running"):
		return {"ip": obj["ip"] ,"port" : obj["port"] , "instance_id" : obj["instance_id"]}
	else:
		return "service not found"

#monitor will hit this api when it does not get a heartbeat from a service
@app.route("/service_dead", methods = ["POST"])
def dead_service():
	data = request.json
	name = data.instance_id
	
	obj = sv.fetchdb({"instance_id" : name })

	sv.updatedb({"service_name" : name }, {"state" : "dead"})
	
	# restart
	# if obj.service_type ==  "platform_service":
		
	# else:
	return "ok"

@app.route("/get_services/<stype>")
def get_services(stype):
	if stype == "running":
		data =sv.fetchdb({"state" : "running"})
		lst = []
		for x in data:
			lst.append([x.service_id,x.service_type,x.service_name])
		return  lst
	elif stype == "killed":
		data = sv.fetchdb({"state" : "scheduled"})
		lst = []
		for x in data:
			lst.append([x.service_id,x.service_type,x.service_name])
		return  lst
	else:
		return "invalid type"




if __name__ == '__main__':
	t1 = threading.Thread(target =consume)
	t1.start()
	app.run(port=PORT, debug=True, )
