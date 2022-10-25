from flask import Flask, request
import service_utilities as sv
import kafka
from json import loads, dumps
import threading
import os
import dotenv
from log_generator import send_log
dotenv.load_dotenv()

PORT = os.getenv('SLCM_service_port')

app = Flask(__name__)

# thread


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
            send_log("INFO", "request recieved from : {}".format(instance))
            obj = sv.fetchdb({"instance_id": instance})
            if obj == None:
                if data["request_type"] == "register":

                    send_log("INFO", "registering : {}".format(instance))
                    # print("saving : ", instance)
                    data["state"] = "running"
                    data.pop("request_type")
                    # print(data)
                    msg = sv.savetodb(data)
                    print("Registered : ", data)
                    if msg == None:
                        msg = "Failed"
                        send_log("ERR", "registration status : {}".format(msg))
                    else:
                        send_log(
                            "INFO", "register update status: {}".format(msg))

            elif data["request_type"] == "unregister":
                msg = sv.updatedb({"instance_id": data["instance_id"]}, {
                                  "state": "stopped"})
                if msg == None:
                    msg = "Failed"
                    send_log("ERR", "unregister update status: {}".format(msg))
                else:
                    send_log("INFO", "unregister update status: {}".format(msg))
            elif data["request_type"] == "register":
                msg = sv.updatedb({"instance_id": data["instance_id"]}, {
                                  "state": "running"})
                if msg == None:
                    msg = "Failed"
                    send_log("ERR", "register update status: {}".format(msg))
                else:
                    send_log("INFO", "register update status: {}".format(msg))

        except:
            send_log("ERR", "ERROR while processing register/unregister request ")


# hit by service to get port of another service
@app.route("/service_lookup", methods=["POST"])
def service_lookup():
    request_data = request.get_json()
    try:
        ser = request_data["service_id"]
        slug = request_data.get("slug")
        if slug is None:
            slug = ""
    except:
        send_log("ERR", "key error : service_id not found in request")
        return {"msg": "key error : service_id not found in request"}, 400
    try:
        sertype = request_data["service_type"]
        obj = sv.fetchdb({"instance_id": ser, "service_type": sertype})
    except:
        obj = sv.fetchdb({"instance_id": ser})
    
    print(obj)

    try:
        if obj is not None:
            if(obj["state"] == "running"):
                url = obj["service_ip"]+":"+obj["service_port"]
                if(url[-1] != '/'):
                    url = url + "/"+slug
                else:
                    url += slug

                send_log("INFO", "returned : {}".format(url))
                return {"msg": "Runnning", "url": url, "kafka": None, "node": obj.node, "instance_id": obj["instance_id"]}, 200
            elif(obj["state"] == "stopped"):
                send_log("WARN", "Service not running : {}".format(
                    obj["instance_id"]))
                return {"msg": "NotRunning"}, 400
        else:
            print(ser, " NOt found")
            send_log("WARN", "Service not found : {}".format(
                request_data["service_id"]))
            return {"msg": "NotFound"}, 400
    except Exception as e:
        send_log("ERR", "ERROR in Servicelookup ")
        return {"msg": "Exception : " + str(e)}, 400

# monitor will hit this api when it does not get a heartbeat from a service


@app.route("/service_dead", methods=["POST"])
def dead_service():
    data = request.json
    # print(data)
    name = data['instance_id']
    obj = sv.fetchdb({"instance_id": name})
    # print("obj ", obj)
    if obj == None:
        send_log("ERR", "NO such service")
        return "NO such service"

    try:
        if(obj.state == "running"):
            sv.updatedb({"instance_id": name}, {"state": "stopped"})

            produce = kafka.KafkaProducer(bootstrap_servers=sv.kafka_bootstrap,
                                          value_serializer=lambda v: dumps(v).encode('utf-8'))
            if obj.service_type == "app":
                # to schedular add the request to ususal pipeline
                produce.send('service_dead_app', {
                             'instance_id': obj.instance_id})
                send_log(
                    "INFO", "Restart request for {} sent to schedular".format(obj.instance))
            elif obj.service_type == "model":
                # to deployer  as deployer has access to the location of the models
                produce.send('service_dead_model', {
                             'service_id': obj.instance_id})
                send_log(
                    "INFO", "Restart request for {} sent to deployer".format(obj.instance))
            return "ok"
        send_log("WARN", "Service not running")
        return "not running"
    except:
        send_log("ERR", "ERROR in dead_service")


@app.route("/change_count", methods=["POST"])
def change_count():
    data = request.json
    instanceid = data['service_id']
    if data['type'] == "increment":
        try:
            fd = sv.fetchdb({"instance_id": instanceid})
            sv.updatedb({"instance_id": instanceid},
                        {"usedby": fd['usedby'] + 1})
            return "success", 200
        except:
            send_log("ERR", "error incrementing " + instanceid)
            return "failure", 500
    elif data['type'] == "decrement":
        try:
            fd = sv.fetchdb({"instance_id": instanceid})
            sv.updatedb({"instance_id": instanceid}, {
                        "usedby": max(0, fd['usedby'] - 1)})
            return {"result": fd['usedby']-1}, 200
        except:
            send_log("ERR", "error decrementing")
            return "failure", 500
    else:
        return "invalid request", 400


@app.route("/get_services/<stype>")
def get_services(stype):
    if stype == "running":
        data = sv.fetchdb({"state": "running"})
        lst = []
        for x in data:
            lst.append([x.service_id, x.service_type, x.service_name])
        return lst
    elif stype == "stopped":
        data = sv.fetchdb({"state": "stopped"})
        lst = []
        for x in data:
            lst.append([x.service_id, x.service_type, x.service_name])
        return lst
    else:
        return "invalid type"


@app.route("/")
def fun():
    return "slcm"


if __name__ == '__main__':
    t1 = threading.Thread(target=consume)
    t1.start()
    send_log("INFO", "SLCM started")
    print("SLCM started")
    app.run(debug=False, port=PORT, host='0.0.0.0')
