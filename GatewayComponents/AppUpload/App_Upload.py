#from RequestManager import db,app
from flask import jsonify,request, render_template
from requests import NullHandler 
import zipfile
from pathlib import Path
import re
import json
import shutil
from AppUpload.validate import *
from Utilities.models import applications
from mongoengine.queryset.visitor import Q
from pathlib import Path
from Utilities.azure_config import *
import time

#PATH = os.path.dirname(__file__)/'Utilities/ApplicationCode' #Mandatory folder

PATH1 = os.path.dirname(__file__)+"/../"
p1="Utilities/ApplicationCode"
PATH=os.path.join(PATH1,p1)

def get_app_instance_id():
    id = "AI_"+ str(int(time.time()))
    return id


def isValid(tar,r_zip):
    #db.createCollection("appliations")
    var1=tar+"/"+"contract.json"
    temp_file_present = file_present(tar,"contract.json")
    if(temp_file_present['status']==1):
        temp_val_contract = validate_contract(var1)
        if(temp_val_contract['status'] == 1):
            if applications.objects(appName=r_zip).count()>0:
                return {"err_msg":"application already in database."}
            else:
                #new_app = applications(app_id,r_zip,tar)
                try:
                    file_data=""
                    with open(tar+"/"+'contract.json') as f:
                        file_data = json.load(f)
                    if file_data:
                        print("\n\n\FIle Read...................\n\n\n", type(file_data))
                    new_app = applications(
                    _id=get_app_instance_id(),
                    appName = r_zip,
                    path = AZURE_APP_PATH+"/"+r_zip,
                    contract = json.dumps(file_data),
                    )
                    
                    new_app.save()
                except Exception as e:
                    print("||||||||\n\n\n |||||||||||||")
                    return {"err_msg":e}
                print(new_app)
                #return render_template('index.html',suc_msg="SUCCESS:application data is added sucessfully.")
                return {"succ_msg":"Valid Zip"}
        else:
            return temp_val_contract
        # else:
        #     return temp_file_present
    else:
        return temp_file_present

def extract_file(input_file):
    with zipfile.ZipFile(input_file,"r") as zip_ref:
        Path_out = PATH1+'Utilities/ApplicationZip'
        print(Path_out)
        zip_ref.extractall(Path_out)
        print("yes..line 50")
    return

def get_sensor_list(tar):
    sensor_list = []
    with open(tar+"/"+'contract.json') as f:
        file_data = json.load(f)
        for i in file_data['sensors']:
            sensor_list.append(i['sensorid'])
    f.close()
    return sensor_list


def create_platform_utility(sensor_list,tar):
    utility_file = open(PATH1+'Utilities/platform_utility.py', 'r')
    utility_template = utility_file.read()
    new_utility_file = open(tar+"/"+'platform_utility.py','w')
    utility_template = re.sub(r"'<sensor_ids>'",str(sensor_list), utility_template)
    new_utility_file.write(utility_template)
    new_utility_file.close()
    utility_file.close()
    return 1

def create_docker(input_file,tar):
    docker_file = open(PATH1+'Utilities/Dockerfile', 'r')
    docker_template = docker_file.read()
    new_docker_file = open(tar+"/"+'Dockerfile','w')
    docker_template = re.sub(r'<app_name>',input_file, docker_template)
    new_docker_file.write(docker_template)
    new_docker_file.close()
    docker_file.close()
    return 1

def create_zip(r_zip,tar):
    os.remove(tar+"/"+'contract.json')
    my_file=shutil.make_archive(r_zip, 'zip', tar)
    print(type(my_file))
    create_dir(AZURE_APP_PATH,r_zip)
    temp_path = AZURE_APP_PATH + "/" + r_zip
    temp_file = r_zip + ".zip"
    upload_file(temp_path,temp_file,r_zip,'application/zip')
    os.remove(temp_file)
    location1="Utilities/ApplicationZip/"
    location2="Utilities/ApplicationCode/"
    r_zip1=r_zip+".zip"
    print(PATH)
    path1=PATH1+location1
    path2=PATH1+location2
    print(path1)
    path1 = os.path.join(path1, r_zip)
    path2 = os.path.join(path2, r_zip1)
    print(path1)
    print(path2)
    shutil.rmtree(path1)
    os.remove(path2) 


def upload_app_file(request):
    err_msg=""
    success_msg=""
    #print(PATH)
    if 'app' not in request.files:
    #if request.files:
        print("no file")
        return 'No file found.'
    f = request.files['app']
    print(PATH)
    f.save(PATH +"/"+f.filename)
    input_file=PATH +"/"+f.filename
    r_zip=Path(f.filename).stem
    #print(input_file)
    if(zipfile.is_zipfile(input_file)):
        extract_file(input_file)
    else:
        return {"err_msg":"ERR:only zip files allowed."}
    tar=PATH1+"Utilities/ApplicationZip" +"/"+r_zip
    
    resp=isValid(tar,r_zip)

    print(resp,"line 89")
    if 'succ_msg' in resp:
        sensor_list = get_sensor_list(tar)
        print("Sensors: ", sensor_list)
        if(create_platform_utility(sensor_list,tar)) and (create_docker(r_zip,tar)):
            create_zip(r_zip,tar)
            return {"succ_msg":"SUCCESS:application data is added sucessfully."}
    else:
        return resp
