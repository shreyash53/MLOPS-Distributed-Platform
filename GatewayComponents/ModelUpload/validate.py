import json
import os.path
from os import path

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
            if(i == "procedures"):
                for j in data[i]:
                    procedure_temp = procedures_validate(j)
                    if procedure_temp['status'] == 0:
                        return procedure_temp
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


def procedures_validate(data):
    key = ["name", "parameters", "return_type"]
    check_key = key_exist_2(data, key)
    if check_key['status'] == 1:
        check_data = data_exist(data, ["name"])
        return check_data
    else:
        return check_key


def validate_contract(contract):
    #    contract = 'contract.json'
    contract_file = open(contract)
    contract_data = json.load(contract_file)

    key = ["model_name", "pickle_file_name", "procedures"]
    contract_key = key_exist(contract_data, key)
    if contract_key['status'] == 1:
        contract_data =  data_exist(contract_data, key)
        if contract_data['status']==1:
            return succ("Good to go!!")
        else:
            return contract_data

    else:
        return contract_key


def file_present(p, fileName):
    p = p/fileName
    if path.exists(p) == False:
        err = error(fileName, "File Not Found")
        return err
    else:
        return succ("File Present")