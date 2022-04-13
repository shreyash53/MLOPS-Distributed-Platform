#from RequestManager import db,app
from flask import jsonify,request, render_template
from requests import NullHandler 
import zipfile
from pathlib import Path
import re
import json
import shutil
from ModelUpload.validate import *
from Utilities.models import aimodels
from mongoengine.queryset.visitor import Q
from pathlib import Path
from Utilities.azure_config import *
import time

# PATH = Path.cwd()/'Utilities/ModelCode' #Mandatory folder
# mydir=Path.cwd()/'NewZip'
PATH1 = os.path.dirname(__file__)+"/../"
# j=len(PATH1)
# while PATH1[j-1]!='/':
#     j=j-1
# PATH1 = PATH1[0,j]
p1="Utilities/ModelCode"
PATH=os.path.join(PATH1,p1)
#PATH=PATH1+p1

def get_model_instance_id():
    id = "MI_"+ str(int(time.time()))
    return id

def isValid(tar,r_zip):
    var1=tar+"/"+"contract.json"
    temp_file_present = file_present(tar,"contract.json")
    if(temp_file_present['status']==1):
        temp_file_present = file_present(tar,"model.pkl")
        if(temp_file_present['status']==1):
            temp_val_contract = validate_contract(var1)
            if(temp_val_contract['status'] == 1):
                #if db.applications.find( { "appName": r_zip } ).count() > 0:
                if aimodels.objects(modelName=r_zip).count()>0:
                    return {"err_msg":"model already in database."}
                else:
                    #new_app = applications(app_id,r_zip,tar)
                    try:
                        file_data=""
                        with open(tar+"/"+'contract.json') as f:
                            file_data = json.load(f)
                        print(file_data)
                        new_app = aimodels(modelId=get_model_instance_id(),
                        modelName = r_zip,
                        path = AZURE_MODEL_PATH+"/"+r_zip,
                        contract = json.dumps(file_data)
                        )
                        new_app.save()
                    except Exception as e:
                        return {"err_msg":e}

                    print(new_app)
                    #return render_template('index.html',suc_msg="SUCCESS:application data is added sucessfully.")
                    return {"succ_msg":"Valid Zip"}
            else:
                return temp_val_contract["err_msg"]
        else:
            return temp_file_present["err_msg"]
    else:
        return temp_file_present["err_msg"]

# def isValid(tar,r_zip):
#     file_data=""
#     with open(tar/'contract.json') as f:
#         file_data = json.load(f)
#     print(file_data)
#     new_app = aimodels(modelName = r_zip,
#                      path = AZURE_MODEL_PATH+"/"+r_zip,
#                      contract = json.dumps(file_data)
#                     )
#     new_app.save()
#     print("valid: line 53")
#     return {"succ_msg":"Valid Zip"}

def extract_file(input_file):
    with zipfile.ZipFile(input_file,"r") as zip_ref:
        Path_out = PATH1+'Utilities/ModelZip'
        print(Path_out)
        zip_ref.extractall(Path_out)
        print("printed..line 60")
    return

def create_docker(input_file,tar):
    docker_file = open(PATH1+'Utilities/Dockerfile', 'r')
    docker_template = docker_file.read()
    new_docker_file = open(tar+"/"+'Dockerfile','w')
    docker_template = re.sub(r'<app_name>',"model_api", docker_template)
    new_docker_file.write(docker_template)
    new_docker_file.close()
    docker_file.close()
    return 1

def create_zip(r_zip,tar):
    #os.remove(tar/'contract.json')
    shutil.make_archive(r_zip, 'zip',tar)
    #upload this zip to my folder.
    create_dir(AZURE_MODEL_PATH,r_zip)
    temp_path = AZURE_MODEL_PATH + "/" + r_zip
    temp_file = r_zip + ".zip"
    upload_file(temp_path,temp_file,r_zip,'application/zip')
    os.remove(temp_file)
    location1="Utilities/ModelZip/"
    location2="Utilities/ModelCode/"
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
    return

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
    tokens['preprocess_fun_parameters'] = ""
    tokens['postprocess_fun_parameters'] = ""
    tokens['predict_fun_parameters'] = ""
    tokens['pickle_file_path'] = contract['pickle_file_name']
    for val in contract["procedures"]:
        if val['name'] == "preprocessing":
            tokens['preprocess_fun_name'] = val['name']
            tokens['preprocess_fun_parameters'] = ""
            tokens['preprocess_return']=val['return_type']
            for j in val['parameters']:
                tokens['preprocess_fun_parameters']+= j['name'] + ", "
                # tokens['preprocess_fun_parameters']+= j['type'] + ","
            tokens['preprocess_fun_parameters'] = tokens['preprocess_fun_parameters'][:-2]
            

        elif val['name'] == "postprocessing":
            tokens['postprocess_fun_name'] = val['name']
            tokens['postprocess_fun_parameters'] = ""
            tokens['postprocess_return']=val['return_type']
            for j in val['parameters']:
                tokens['postprocess_fun_parameters']+= j['name'] + ", "
                # tokens['postprocess_fun_parameters']+= j['type'] + ","
            tokens['postprocess_fun_parameters'] = tokens['postprocess_fun_parameters'][:-2]

        elif val['name'] == "predict":
            tokens['predict_fun_name'] = val['name']
            tokens['predict_fun_parameters'] = ""
            tokens['predict_return']=val['return_type']
            for j in val['parameters']:
                tokens['predict_fun_parameters']+= j['name'] + ", "
                # tokens['predict_fun_parameters']+= j['type'] + ","
            tokens['predict_fun_parameters'] = tokens['predict_fun_parameters'][:-2]

    # tokens['preprocess_fun_name'] = contract['pre_processing_fun']['name']
    # tokens['postprocess_fun_name'] = contract['post_processing_fun']['name']
    # tokens['predict_fun_name'] = contract['predict_fun']['name']

    model_api = re.sub(r'<other_dependencies>',
                       tokens['other_dependencies'], model_api)
    model_api = re.sub(r'<pickle_file_path>',
                       tokens['pickle_file_path'], model_api)
    
    #updating function name
    model_api = re.sub(r'<preprocess_fun_name>',
                       tokens['preprocess_fun_name'], model_api)
    model_api = re.sub(r'<postprocess_fun_name>',
                       tokens['postprocess_fun_name'], model_api)
    model_api = re.sub(r'<predict_fun_name>',
                       tokens['predict_fun_name'], model_api)
    
    #updating parameters list
    model_api = re.sub(r'<preprocessing_para_name>',
                       tokens['preprocess_fun_parameters'], model_api)
    model_api = re.sub(r'<predict_para_name>',
                       tokens['predict_fun_parameters'], model_api)
    model_api = re.sub(r'<postprocessing_para_name>',
                       tokens['postprocess_fun_parameters'], model_api)


    api_file.write(model_api)
    api_file.close()

def upload_model_file(request):
    err_msg=""
    success_msg=""
    #print(PATH)
    if request.files['model'].filename == '':
    #if request.files:
        print("no file")
        return {"err_msg":"ERR:No file uploaded"}
    f = request.files['model']

    f.save(PATH+"/"+f.filename)
    input_file=PATH +"/"+f.filename
    r_zip=Path(f.filename).stem
    #print(input_file)
    if(zipfile.is_zipfile(input_file)):
        extract_file(input_file)
    else:
        return {"err_msg":"ERR:only zip files allowed."}
    tar=PATH1+"Utilities/ModelZip" +"/"+r_zip
    resp=isValid(tar,r_zip)
    print(resp,"line 89")
    if 'succ_msg' in resp:
        # generate_model_api(tar)
        if(create_docker(r_zip,tar)):
            print("done create model")
            create_zip(r_zip,tar)
            return {"succ_msg":"SUCCESS:model data is added sucessfully."}
    else:
        return {"err_msg":resp}