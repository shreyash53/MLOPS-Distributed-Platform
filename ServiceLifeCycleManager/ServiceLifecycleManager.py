from flask import Flask, request
import service_utilities as sv
import kafka
from json import loads,dumps
import threading
import dotenv
import os
dotenv.load_dotenv()

app = Flask(__name__)

def consume():
	consumer = kafka.KafkaConsumer(
    'register',
    bootstrap_servers=[sv.kafka_bootstrap],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

	for message in consumer:
		try:
			data = message.value
			instance = data["instance_id"]
			print("request recieved from : ",instance)
			obj = sv.fetchdb({"instance_id" : instance})
			if obj == None :
				if data["request_type"] == "register":
					print("saving : ", instance)
					data["state"] = "running"
					data.pop("request_type")
					# print(data)
					print(sv.savetodb(data))

			elif data["request_type"] == "unregister":
				sv.updatedb({"instance_id"  : data["instance_id"]} , {"state" :"stopped" })
			elif data["request_type"] == "register":
				sv.updatedb({"instance_id"  : data["instance_id"]} , {"state" :"running" })
				print("updated")
		except : 
			pass

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
	ser=request_data["service_id"]
	try:
		sertype = request_data["service_type"]
	except:
		pass
	try:
		slug = request_data["slug"]
	except:
		slug = ""


	obj = sv.fetchdb({"instance_id" :ser , "service_type" : sertype })
	if obj:
		obj = obj.first()
		if(obj!=None and obj["state"] == "running"):
			url ="http://"+obj["ip"]+":"+obj["port"]+slug
			return {"msg" : "Runnning" , "url": url ,"kafka" : None ,"node" : obj.nodeid, "instance_id" : obj["instance_id"]},200
		elif(obj!=None and obj["state"] == "stopped"):
			return {"msg" : "NotRunning"},400
	else:
		return {"msg" : "NotFound"},400

#monitor will hit this api when it does not get a heartbeat from a service
@app.route("/service_dead", methods = ["POST"])
def dead_service():
	data = request.json
	print(data)
	name = data['instance_id']
	obj = sv.fetchdb({"instance_id" : name })
	print("obj ", obj)
	if obj == None:
		return "NO such service"
	print("asd")

	if(obj.state == "running"):
		sv.updatedb({"instance_id" : name }, {"state" : "stopped"})
	
		produce = kafka.KafkaProducer(bootstrap_servers=sv.bootstrap_servers,
                          value_serializer=lambda v: dumps(v).encode('utf-8'))
		if obj.service_type == "application":
			produce.send('service_dead_app', {'instance_id' : obj.instance_id})# to schedular add the request to ususal pipeline
		elif obj.service_type == "model":
			produce.send('service_dead_model',{'instance_id' : obj.instance_id})# to deployer  as deployer has access to the location of the models
		

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
	elif stype == "stopped":
		data = sv.fetchdb({"state" : "stopped"})
		lst = []
		for x in data:
			lst.append([x.service_id,x.service_type,x.service_name])
		return  lst
	else:
		return "invalid type"
@app.route("/")
def fun():
	return "slcm"



if __name__ == '__main__':
	t1 = threading.Thread(target =consume)
	t1.start()
	print("started")
	app.run(port=sv.PORT,host = sv.HOST )
