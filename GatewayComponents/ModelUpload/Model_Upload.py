#from RequestManager import db,app
from flask import jsonify,request, render_template
from requests import NullHandler 
import zipfile
from pathlib import Path
import re
import json
import shutil
from AppUpload.validate import *
from Utilities.models import aimodels
from mongoengine.queryset.visitor import Q
from pathlib import Path

PATH = Path.cwd()/'Utilities/ModelCode' #Mandatory folder
mydir=Path.cwd()/'NewZip'
# def isValid(tar,r_zip):
#     #db.createCollection("models")
#     var1=tar/"contract.json"
#     if(file_present(tar,"contract.json")):
#         if(file_present(tar,"run.sh")):
#             if(validate_contract(var1)):
#                 print("hello")
#                 #if db.models.find( { "appName": r_zip } ).count() > 0:
#                 if models.objects(appName=r_zip).count()>0:
#                     return {"err_msg":"model already in database."}
#                 else:
#                     #new_app = models(app_id,r_zip,tar)
#                     try:
#                         new_app = models(
#                         modelName = r_zip,
#                         #pickleName = 
#                         path = str(tar)
#                         )
#                         new_app.save()
#                     except Exception as e:
#                         return {"err_msg":e}

#                     print(new_app)
#                     #return render_template('index.html',suc_msg="SUCCESS:application data is added sucessfully.")
#                     return {"succ_msg":"Valid Zip"}
#             else:
#                 return {"err_msg":"ERR:contract.json seems invalid."}
#         else:
#             return {"err_msg":"ERR:run.sh not present."}
#     else:
#         return {"err_msg":"ERR:contract.json not present."}

def isValid(tar,r_zip):
    file_data=""
    with open(tar/'contract.json') as f:
        file_data = json.load(f)
    print(file_data)
    new_app = aimodels(modelName = r_zip,
                     path = str(tar),
                     contract = json.dumps(file_data)
                    )
    new_app.save()
    print("valid: line 53")
    return {"succ_msg":"Valid Zip"}

def extract_file(input_file):
    with zipfile.ZipFile(input_file,"r") as zip_ref:
        Path_out = Path.cwd()/'Utilities/ModelZip'
        zip_ref.extractall(Path_out)
        print("printed..line 60")
    return

def create_docker(input_file,tar):
    docker_file = open(Path.cwd()/'Utilities/Dockerfile', 'r')
    docker_template = docker_file.read()
    new_docker_file = open(tar/'Dockerfile','w')
    docker_template = re.sub(r'<app_name>',"model_api", docker_template)
    new_docker_file.write(docker_template)
    new_docker_file.close()
    docker_file.close()
    return 1

def create_zip(tar):
    #os.remove(tar/'contract.json')
    shutil.make_archive('zipfile_name', 'zip',tar)
    #upload this zip to my folder.

def generate_model_api(store_path):
    template_file = open('Utilities/model_api.py', 'r')
    model_api = template_file.read()
    api_file = open(os.path.join(store_path, 'model_api.py'), 'w')

    contract_path = os.path.join(store_path, 'contract.json')
    contract_file = open(contract_path)
    contract = json.loads(contract_file.read())

    tokens = {'other_dependencies': '',
              'pickle_file_path': '',
              'preprocess_fun_name': '',
              'predict_fun_name': '',
              'postprocess_fun_name': '',
              }

    for vals in contract['dependencies']:
        tokens['other_dependencies'] += '\n' + vals

    tokens['pickle_file_path'] = contract['pickle_file_name']
    tokens['preprocess_fun_name'] = contract['pre_processing_fun']['name']
    tokens['postprocess_fun_name'] = contract['post_processing_fun']['name']
    tokens['predict_fun_name'] = contract['predict_fun']['name']

    model_api = re.sub(r'<other_dependencies>',
                       tokens['other_dependencies'], model_api)

    model_api = re.sub(r'<pickle_file_path>',
                       tokens['pickle_file_path'], model_api)
    model_api = re.sub(r'<preprocess_fun_name>',
                       tokens['preprocess_fun_name'], model_api)
    model_api = re.sub(r'<postprocess_fun_name>',
                       tokens['postprocess_fun_name'], model_api)
    model_api = re.sub(r'<predict_fun_name>',
                       tokens['predict_fun_name'], model_api)

    api_file.write(model_api)
    api_file.close()

def upload_model_file(request):
    err_msg=""
    success_msg=""
    #print(PATH)
    if 'model' not in request.files:
    #if request.files:
        print("no file")
        return 'No file found.'
    f = request.files['model']

    f.save(PATH /f.filename)
    input_file=PATH /f.filename
    r_zip=Path(f.filename).stem
    #print(input_file)
    if(zipfile.is_zipfile(input_file)):
        extract_file(input_file)
    else:
        return {"err_msg":"ERR:only zip files allowed."}
    tar=Path.cwd()/"Utilities/ModelZip" /r_zip
    resp=isValid(tar,r_zip)
    print(resp,"line 89")
    if 'succ_msg' in resp:
        generate_model_api(tar)
        if(create_docker(r_zip,tar)):
            create_zip(tar)
            return {"succ_msg":"SUCCESS:model data is added sucessfully."}
    return {"err_msg":"Invalid Zip"}