import json
import os.path
from os import path
import requests
from Utilities.models import aimodels

URL = 'http://127.0.0.1/sensor_validate'

def error(val, error_name):
    msg = "Key Error: {} {}!".format(val, error_name)
    temp = {
        "msg": msg,
        "status": 0
    }
    print(temp)
    return temp


def succ(msg):
    temp = {
        "msg": msg,
        "status": 1
    }
    print(temp)
    return temp

def key_exist(data,key):
    for i in key:
        if data.get(i) is not None:
            if(i == "sensors"):
                for j in data[i]:
                    sensor_temp = sensors_validate(j)
                    if sensor_temp['status'] == 0:
                        return sensor_temp
                sensor_data = {
                    "Details": data[i]
                }
                res = requests.post(URL,json=sensor_data).content()
                if(res['status']==0):
                    return error(res['sensorid'],"Sensor Type Not Present")
            elif(i == "models"):
                for j in data[i]:
                    model_temp = model_validate(j)
                    if model_temp['status'] == 0:
                        return model_temp
                    if aimodels.object(modelName=data[i]['modelname']).count()==0:
                        return error(data[i]['modelname'],"Not Present")

        else:   
            return error(i,"Not Found")
    return succ("All Keys Present")

def key_exist_2(data, key):
    for i in key:
        if data.get(i) is not None:
            pass
        else:
            return error(i, "Not Found")
    return succ("Found")


def data_exist(data, key):
    for i in key:
        if data[i]:
            pass
        else:
            return error(i, "has no Data")
    return succ("Data Exist")


def sensors_validate(data):
    key = ["sensorname", "sensorid", "sensortype", "sensordatatye"]
    check_key = key_exist_2(data, key)
    if check_key['status'] == 1:
        check_data = data_exist(data, key)
        # if check_data['status']==1:
        return check_data
        # else:
        #     return check_data
    else:
        return check_key


def model_validate(data):
    key = ["modelname", "modelid", "modelloc"]
    check_key = key_exist_2(data, key)
    if check_key['status'] == 1:
        check_data = data_exist(data, key)
        return check_data
        # if data_exist(data, key):
        #     return True
        # else:
        #     return False
    else:
        return check_key


def validate_contract(contract):
    #    contract = 'contract.json'
    contract_file = open(contract)
    contract_data = json.load(contract_file)

    key = ["application_name", "models", "sensors"]
    contract_key = key_exist(contract_data, key)
    if contract_key['status'] == 1:
        contract_data =  data_exist(contract_data, key)
        if contract_data['status']==1:
            return succ("Good to go!!")
        else:
            return contract_data

    else:
        return contract_key
        # print("Upload With Valid contract.json")


def file_present(p, fileName):
    p = p/fileName
    if path.exists(p) == False:
        err = error(fileName, "File Not Found")
        return err
    else:
        return succ("File Present")
