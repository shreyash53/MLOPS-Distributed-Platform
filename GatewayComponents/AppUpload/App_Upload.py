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

PATH = Path.cwd()/'Utilities/ApplicationCode' #Mandatory folder

def isValid(tar,r_zip):
    #db.createCollection("applications")
    var1=tar/"contract.json"
    if(file_present(tar,"contract.json")):
        if(file_present(tar,"run.sh")):
            if(validate_contract(var1)):
                print("hello")
                #if db.applications.find( { "appName": r_zip } ).count() > 0:
                if applications.objects(appName=r_zip).count()>0:
                    return {"err_msg":"application already in database."}
                else:
                    #new_app = applications(app_id,r_zip,tar)
                    try:
                        new_app = applications(
                        appName = r_zip,
                        path = str(tar)
                        )
                        new_app.save()
                    except Exception as e:
                        return {"err_msg":e}

                    print(new_app)
                    #return render_template('index.html',suc_msg="SUCCESS:application data is added sucessfully.")
                    return {"succ_msg":"Valid Zip"}
            else:
                return {"err_msg":"ERR:contract.json seems invalid."}
        else:
            return {"err_msg":"ERR:run.sh not present."}
    else:
        return {"err_msg":"ERR:contract.json not present."}

def extract_file(input_file):
    with zipfile.ZipFile(input_file,"r") as zip_ref:
        Path_out = Path.cwd()/'Utilities/ApplicationZip'
        zip_ref.extractall(Path_out)
        print("yes..line 50")
    return

def create_docker(input_file,tar):
    docker_file = open(Path.cwd()/'Utilities/Dockerfile', 'r')
    docker_template = docker_file.read()
    new_docker_file = open(tar/'Dockerfile','w')
    docker_template = re.sub(r'<app_name>',input_file, docker_template)
    new_docker_file.write(docker_template)
    new_docker_file.close()
    docker_file.close()
    return 1

def create_zip(tar):
    os.remove(tar/'contract.json')
    shutil.make_archive('zipfile_name', 'zip', tar)
    #upload this zip to my folder.

def upload_app_file(request):
    err_msg=""
    success_msg=""
    #print(PATH)
    if 'app' not in request.files:
    #if request.files:
        print("no file")
        return 'No file found.'
    f = request.files['app']

    f.save(PATH /f.filename)
    input_file=PATH /f.filename
    r_zip=Path(f.filename).stem
    #print(input_file)
    if(zipfile.is_zipfile(input_file)):
        extract_file(input_file)
    else:
        return {"err_msg":"ERR:only zip files allowed."}
    tar=Path.cwd()/"Utilities/ApplicationZip" /r_zip
    resp=isValid(tar,r_zip)
    print(resp,"line 89")
    if 'succ_msg' in resp:
        if(create_docker(r_zip,tar)):
            create_zip(tar)
            return {"succ_msg":"SUCCESS:application data is added sucessfully."}
    return {"err_msg":"Invalid Zip"}
