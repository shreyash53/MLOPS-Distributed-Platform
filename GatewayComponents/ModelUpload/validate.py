import json
import os.path
from os import path


def error(val, error_name):
    '''
    Function to return error
    val: key in which error is there
    error_name: name of the error
    '''
    msg = "Key Error: {} {}!".format(val, error_name)
    temp = {
        "err_msg": msg,
        "status": 0
    }
    print(temp)
    return temp


def succ(msg):
    '''
    msg: message to return on success
    '''
    temp = {
        "succ_msg": msg,
        "status": 1
    }
    print(temp)
    return temp


def key_exist(data, key):
    '''
    data: json data
    key: all the keys inside json
    '''
    for i in key:
        if data.get(i) is not None:
            if(i == "procedures"):
                for j in data[i]:
                    procedure_temp = procedures_validate(j)
                    if procedure_temp['status'] == 0:
                        return procedure_temp
        else:
            return error(i, "Not Found")
    return succ("All Keys Present")


def key_exist_2(data, key):
    '''
    data: sub_keys data
    key: keys of subdata

    '''
    for i in key:
        if data.get(i) is not None:
            pass
        else:
            return error(i, "Not Found")
    return succ("Found")


def data_exist(data, key):
    '''
    Fuction  to check wheter data is present in keys
    '''
    for i in key:
        if data[i]:
            pass
        else:
            return error(i, "has no Data")
    return succ("Data Exist")


def procedures_validate(data):
    '''
    function to validate all the function related keys
    '''
    key = ["name", "parameters", "return_type"]
    check_key = key_exist_2(data, key)
    if check_key['status'] == 1:
        check_data = data_exist(data, ["name"])
        return check_data
    else:
        return check_key


def validate_contract(contract):
    #    contract = 'contract.json'
    '''
    Function to validate model contract
    '''
    contract_file = open(contract)
    contract_data = json.load(contract_file)

    key = ["model_name", "pickle_file_name", "procedures", "dependencies"]
    contract_key = key_exist(contract_data, key)
    if contract_key['status'] == 1:
        contract_data = data_exist(contract_data, key)
        if contract_data['status'] == 1:
            return succ("Good to go!!")
        else:
            return contract_data

    else:
        return contract_key


def file_present(p, fileName):
    '''
    Function to check file is present in current path or not
    p:path
    fileName: file to check
    '''

    p = p+"/"+fileName
    if path.exists(p) == False:
        err = error(fileName, "File Not Found")
        return err
    else:
        return succ("File Present")
