from fileinput import filename
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from sensor_bind.sensor_binder import *
from sensor_register.sensor_reg import *
from flask import jsonify, make_response, render_template
from mongoengine.connection import connect
import requests
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import json
from dbconfig import *

app = Flask(__name__)
db = mongodb()

# username = "root"
# password="2"
# server = "localhost:9001"
# # note an error here

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/SensorDB'%password
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "/home/pulkit/IAS NEW/sensor_manager/"

# s = "mysql+pymysql://{}:{}@{}/db".format(username, password, server)
# print(s)

# app.config["SQLALCHEMY_DATABASE_URI"] = s

# db = SQLAlchemy(app)
# db.init_app(app)


@app.route('/', methods=["GET", "POST"])
def form():
    return render_template('form.html')

@app.route("/Sensor_Register", methods=["GET","POST"])
def Sensor_Reg():
    sensor_reg_data=request.json
    ret_value = reg_sensor(sensor_reg_data)
    return ret_value


@app.route('/upload', methods=["GET", "POST"])
def upload():
    file_name = request.files['File'].filename
    # file_name = 'abc.json'
    s="sensor_bind"
    filepath = Path.cwd() / s / file_name
    # print(filepath)
    url = "http://localhost:9002/get_file"
    file_data = {'file': filepath.open(mode='rb')}
    r = requests.post(url, files=file_data).content
    jsonResponse = json.loads(r.decode('utf-8'))
    url = "http://localhost:9002/Sensor_Bind"
    res = requests.post(url, json=jsonResponse).content
    return res


@app.route('/get_file', methods=["POST", "GET"])
def get_file():
    file = request.files['file']
    if file:
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        f = open(file_name, "r")
        data = json.loads(f.read())
        data = json.dumps(data)
        f.close()
        os.remove(file_name)
        return data

@app.route("/Sensor_Bind", methods=["POST","GET"])
def Sensor_Bind():
    request_data = request.json
    # print(request_data)
    ret_value = reg_bind_sensor(request_data)
    return ret_value

@app.route("/Check_From_Runner", methods=["POST", "GET"])
def Check_Run():
    request_data = request.json
    ret_value = Check(request_data)    
    return ret_value

@app.route("/Run_All_Sensors", methods=["POST", "GET"])
def Run_All():
    request_data = request.json
    url = "ip:port/service_lookup"
    for i in request_data["s_id"]:
        val={"service_name":i}
        r = requests.post(url, json=jsonify(val)).content
        if(r==-1):
            res=start_sensor(val)
            url2 = "ip:port/start_service"
            requests.post(url2, json=res).content
            sensor_add_db(val)
        else:
            sensor_add(val)
            
@app.route("/Get_Data", methods=["POST", "GET"])
def Get_Data():
    request_data = request.json




# with app.app_context():
#     db.create_all()

    

