from fileinput import filename
from flask import Flask,request
# from flask_sqlalchemy import SQLAlchemy
from sensor_bind.sensor_binder import *
from flask import jsonify, make_response, render_template
from mongoengine.connection import connect
import requests
from pathlib import Path
from werkzeug.utils import secure_filename
from dbconfig import *
# import os
# import json

app = Flask(__name__)
db = mongodb()


@app.route("/Sensor_Bind", methods=["POST","GET"])
def Sensor_Bind():
    request_data = request.json
    # print(request_data)
    ret_value = reg_bind_sensor(request_data)
    data={}
    data["Message"]=ret_value
    return data

@app.route("/Get_Data", methods=["GET"])
def Get_Data():
    a=Check_Vals()
    D={}
    D["details"]=a
    return D


@app.route("/sensor_validate", methods=["POST","GET"])
def Check_Dev():
    request_data = request.json
    i,lis = Check_From_Dev(request_data)
    dic={}
    if i:
            dic["msg"] = "error"
            dic["status"]=0
            dic["sensorid"]=lis[0]
    else:
            dic["msg"] = "Success"
            dic["status"]=1

    return dic
    

@app.route("/Check_From_AppRunner", methods=["POST","GET"])
def Check_Run2():
    request_data = request.json
    print(request_data)
    i,lis1,lis2 = Check_From_Runner(request_data)
    dic={}
    if i:
        dic["error"]=lis1
    else:
        dic["Success_Message"]=lis2
        
    print(dic)
    return jsonify(dic)
# with app.app_context():
#     db.create_all()

    
