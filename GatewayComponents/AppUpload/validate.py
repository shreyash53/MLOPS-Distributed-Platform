import json
import os.path
from os import path

def error(val,error_name):
    print("Key Error: {} {}!".format(val, error_name))

def key_exist(data,key):
    for i in key:
        if data.get(i) is not None:
            if(i == "services"):
                for j in data[i]:
                    if service_validate(j) == False:
                        return False
            elif(i == "sensors"):
                    for j in data[i]:
                        if sensors_validate(j) == False:
                            return False
            elif(i == "models"):
                for j in data[i]:
                    if model_validate(j) == False:
                        return False

        else:   
            error(i,"Not Found")
            return False
    return True

def key_exist_2(data,key):
    for i in key:
        if data.get(i) is not None:
            pass
        else:
            error(i,"Not Found")
            return False
    return True            

def data_exist(data,key):
    for i in key:
        if data[i]:
            pass
        else:
            error(i,"has no Data")
            return False
    return True


def sensors_validate(data):
    key = ["sensorname","sensorid","sensortype"]
    if key_exist_2(data,key):
        if data_exist(data,key):
            return True
        else:
            return False
    else:
        return False

def service_validate(data):
    key = ["servicename","serviceloc"]
    if key_exist_2(data,key):
        if data_exist(data,key):
            return True
        else:
            return False
    else:
        return False

def model_validate(data):
    key = ["modelname","modelid","modelloc"]
    if key_exist_2(data,key):
        if data_exist(data,key):
            return True
        else:
            return False
    else:
        return False


def validate_contract(contract):
#    contract = 'contract.json'
    contract_file = open(contract)
    contract_data = json.load(contract_file)


    key = ["application_name","services","models","sensors"]

    if key_exist(contract_data,key):
        if data_exist(contract_data,key):
            print("Good to go!!")
            return 1
        else:
            print("Data required in all fields!!")

    else:
        print("Upload With Valid contract.json")


def file_present(p,fileName):
    p = p/fileName
    if path.exists(p)==False:
        error(fileName,"File Not Found")
        return False
    else: 
        return True