from flask import Flask, jsonify, redirect, render_template, request
from Authenticate import *
#import mongoengine as db
from AppUpload.App_Upload import *
from ModelUpload.Model_Upload import *
from Utilities.dbconfig import *
import dotenv
# from constant import *
dotenv.load_dotenv() 

app = Flask(__name__)
db=mongodb()

SENSOR_MGR_IP = os.environ.get('sensor_manager_service_ip')
SENSOR_MGR_PORT = os.environ.get('sensor_manager_service_port')
app.config['SECRET_KEY'] = 'root'

from flask import Blueprint
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/app/<uid>/<regex("[a-zA-Z0-9.\/_%?-]*"):slug>')
def example(uid, slug):
    data = {
        "service_id":uid,
        "slug":slug
    }
    print("Data: ",data)
    
    slcm_url = os.environ.get('SLCM_service_ip')+":" + os.environ.get('SLCM_service_port') + '/service_lookup'
    # slcm_url = "http://192.168.96.201:9002/service_lookup"
    res = requests.post(url=slcm_url,json=data)
    if(res.status_code==400):
        return ("Application Not Scheduled!! Please look after sometime!!")
    else :
        res = res.json
        redirect(location=res['url'])

    
    # return "uid: %s, slug: %s" % (uid, slug)



def validate_token(t):
    try:
        data = jwt.decode(t,app.config['SECRET_KEY'],algorithms=['HS256'])
        return True
    except:
        return False

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        try:
            token = request.args.get('token')
            print(token,"LIne 28")
        except:
            return jsonify({'message':'Token is missing 29'}), 401
        # print(token)
        if  not token:
            return jsonify({'message':'Token is missing 32'}), 401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            print( 'JWT verification',data['username'])
            current_user = Actor.objects(username = data['username']).first()
        except:
            return jsonify({'message':'Token is invalid!!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/signup',methods=["GET", "POST"])
def signup_page():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == "POST":
        resp = signup({  'username':request.form['username']  ,  'password':request.form['password']  ,  'role':request.form['role']  })
        if 'succ_msg' in resp:
            return render_template('signup.html',succ_msg=resp['succ_msg'])
        else:
            return render_template('signup.html',err_msg=resp['err_msg'])

@app.route('/', methods=["GET"])
@app.route('/login',methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        resp = login({  'username':request.form['username']  ,  'password':request.form['password']  ,  'role':request.form['role']  })
        return render_template('login.html', ret=resp)

@app.route('/app_developer',methods=["GET","POST"])
# @token_required
def app_developer_view():
# def app_developer_view(current_user):
    # if current_user.role != 'app_developer':
    #     return 'Invalid Request(Role Mismatch)'
    if 'token' in request.args:
        if not validate_token(request.args.get("token")):
            return render_template('login.html',err_msg="Invalid Token.Redirecting to login page")
    
    # sensor_details = [('T1','DT1'),('T2','DT2'),('T1','DT2')]
    # model_details = ['m1','m2','m3']
    url = SENSOR_MGR_IP+ ':'+ str(SENSOR_MGR_PORT)+'/Get_Data'
    sensor_details = requests.get(url=url).json()
    sensor_details = sensor_details['details']
    model_details = aimodels.objects().all()
    model_details = [[i.modelName,i.modelId] for i in model_details]
    print(sensor_details,model_details)
    return render_template('app_developer.html',sensor_details=sensor_details,model_details=model_details)

@app.route('/platform_admin',methods=["GET","POST"])
# @token_required
# def platform_admin_view(current_user):
def platform_admin_view():
    # if current_user.role != 'platform_admin':
    #     return 'Invalid Request(Role Mismatch)'
    if 'token' in request.args:
        if not validate_token(request.args.get("token")):
            return render_template('login.html',err_msg="Invalid Token.Redirecting to login page")
    return render_template('platform_admin.html')

@app.route('/data_scientist',methods=["GET","POST"])
@token_required
def data_scientist_view(current_user):
    # if current_user.role != 'platform_admin':
    #     return 'Invalid Request(Role Mismatch)'
    if 'token' in request.args:
        if not validate_token(request.args.get("token")):
            return render_template('login.html',err_msg="Invalid Token.Redirecting to login page")
    return render_template('data_scientist.html')
    

@app.route('/end_user',methods=["GET","POST"])
@token_required
# def platform_admin_view(current_user):
def end_user_view(current_user):
# def end_user_view():
    # if current_user.role != 'platform_admin':
    #     return 'Invalid Request(Role Mismatch)'
    if 'token' in request.args:
        if not validate_token(request.args.get("token")):
            return render_template('login.html',err_msg="Invalid Token.Redirecting to login page")
    apps = ['a1','a2','a3','a4','a5']
    apps = applications.objects().all()
    if len(apps) != 0:
        apps = [[i._id,i.appName] for i in apps]
    return render_template('end_user.html',apps=apps)
    
@app.route('/protected',methods=['POST'])
@token_required
def protected(current_user):
    return jsonify({"message":"Able to access because token verified", "user":current_user.username , "role":current_user.role}), 200

@app.route('/app_developer/upload_app',methods=['POST'])
@token_required
def upload_app(current_user):
    if current_user.role != 'app_developer':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401   
    print(request.files.lists) 
    resp = upload_app_file(request)
    # sensor_details = [('T1','DT1'),('T2','DT2'),('T1','DT2')]
    url = SENSOR_MGR_IP+ ':'+ str(SENSOR_MGR_PORT)+'/Get_Data'
    sensor_details = requests.get(url=url).json()
    sensor_details = sensor_details['details']
    # sensor_details = [ [i[0],i[1]] for i in sensor_details ]
    # model_details = ['m1','m2','m3']
    model_details = aimodels.objects().all()
    model_details = [[i.modelName,i.modelId] for i in model_details]
    if 'err_msg' in resp:
        return render_template('app_developer.html',sensor_details=sensor_details,model_details=model_details,err_msg=resp['err_msg'])
    elif 'succ_msg' in resp:
        return render_template('app_developer.html',sensor_details=sensor_details,model_details=model_details,succ_msg=resp['succ_msg'])
    return render_template('app_developer.html',sensor_details=sensor_details,model_details=model_details)

@app.route('/data_scientist/upload_model',methods=['POST'])
@token_required
def upload_model(current_user):
    if current_user.role != 'data_scientist':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401    
    resp =upload_model_file(request)
    if 'err_msg' in resp:
        return render_template('data_scientist.html',err_msg=resp['err_msg'])
    elif 'succ_msg' in resp:
        return render_template('data_scientist.html',succ_msg=resp['succ_msg'])
    return render_template('data_scientist.html')

@app.route('/end_user/use_app',methods=['POST'])
@token_required
def use_app(current_user):
    if current_user.role != 'end_user':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401    
    return jsonify({"message":"Able to access because token verified", "user":current_user.username , "role":current_user.role}), 200

@app.route('/platform_admin/upload_sensor',methods=['POST'])
@token_required
def upload_sensor(current_user):
    if current_user.role != 'platform_admin':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401 

    if 'file' not in request.files:
    #if request.files:
        print("no file")
        return 'No file found.'
    f = request.files['file']
    f = json.load(f)
    url="http://"+SENSOR_MGR_IP+"/"+SENSOR_MGR_PORT+"/Sensor_Reg"
    res = requests.post(url,json=f).json()
    print(res)
    return res
    # return jsonify({"message":"Able to access because token verified", "user":current_user.username , "role":current_user.role}), 200

@app.route('/platform_admin/bind_sensor',methods=['POST'])
@token_required
def bind_sensor(current_user):
    if current_user.role != 'platform_admin':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401 

    if 'file' not in request.files:
    #if request.files:
        print("no file")
        return 'No file found.'
    f = request.files['file']
    f = json.load(f)
    url="http://"+SENSOR_MGR_IP+"/"+SENSOR_MGR_PORT+"/Sensor_Bind"
    res = requests.post(url,json=f).json()
    print(res)
    return res
    # return jsonify({"message":"Able to access because token verified", "user":current_user.username , "role":current_user.role}), 200


@app.route('/platform_admin/add_node',methods=['POST'])
@token_required
def add_node(current_user):
    if current_user.role != 'platform_admin':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401    
    
    if 'file' not in request.files:
        print("no file")
        return 'No file found.'
    f = request.files['file']
    f = json.load(f)
    res = requests.post("http://0.0.0.0:6000/node/add",json=f).json()
    return res

@app.route('/end_user/get_app_sensor',methods=['POST'])
@token_required
def get_sensor(current_user):
    appName = request.form.get('apps')
    print("\n\nAPPNAME",appName)
    temp = applications.objects(appName=appName).first()
    temp = temp['contract']
    temp = json.loads(temp)
    to_send = []
    for i in temp['sensors']:
        temp = {
            "sensortype":i['sensortype'],
            "sensordatatype": i['sensordatatype']
        }
        to_send.append(temp)
    url = SENSOR_MGR_IP+ ':'+ str(SENSOR_MGR_PORT)+'/Get_Data'
    sensor_details = requests.get(url=url).json()
    sensor_details = sensor_details['details']
    return render_template("sensor_form.html",app_name = appName,sensors=to_send,sensor_details=sensor_details)

@app.route('/end_user/sensor_bind',methods=['POST'])
@token_required
def sensor_bind(current_user):
    appName = request.form['app_name']
    # count = applications.objects(appName=appName).count()
    temp = applications.objects(appName=appName).first()
    temp = temp['contract']
    temp = json.loads(temp)
    count = len(temp['sensors'])
    to_send = []
    for i in temp['sensors']:
        temp = {
            "sensortype":i['sensortype'],
            "sensordatatype": i['sensordatatype']
        }
        to_send.append(temp)
    temp = []
    req_json=list()
    for i in range (1,int(count)+1):
        temp_dict={
            "Sensor_Type":request.form['sensor_type_'+str(i)],
            "Sensor_loc":request.form['sensor_loc_'+str(i)],
            "Sensor_DType":request.form['sensor_dtype_'+str(i)]
        }
        req_json.append(temp_dict)
    temp_json={"Details":req_json}
    # API call
    url = SENSOR_MGR_IP+ ':'+ str(SENSOR_MGR_PORT)+'/Check_From_AppRunner'
    resp = requests.post(url,json=temp_json).json()
    # resp = resp.decode('utf-8')
    print(resp)
    if "error" in resp:
        return render_template('sensor_form.html',err_msg="Mismatch for sensor type and sensor location for some sensors",sensors=to_send,app_name=appName)
    elif "Success_Message" in resp:
        print("Got from Sensor Manager")
        application = applications.objects(appName=appName).first()
        to_scheduler = {
            "app_name":appName,
            "app_id":application._id,
            "starttime":request.form['starttime'],
            "repetition": request.form['repetition'],
            "interval":{
                "days": request.form['Day'],
                "hours": request.form['Hour'],
                "minutes": request.form['Minute'],
                "seconds": request.form['Second']
            },
            "endtime": request.form['endtime']
        }

        sensor_list=[]
        for i in resp["Success_Message"]:
            t = {
                "sensor_name":i["sensor_name"],
                "sensor_binding_id": i['sensor_bind_id']
            }
            sensor_list.append(t)
        print("Sensor List Line 302 \n",sensor_list)
        
        to_scheduler["sensors"] = sensor_list
        url = "http://0.0.0.0:8001/schedule_application"
        # url = "http://192.168.96.240:7000/schedule_application"
        res = requests.post(url,json=to_scheduler).json()
        if 'err_msg' in res:
            return  render_template('sensor_form.html',err_msg=res['err_msg'],sensors=to_send,app_name=appName)
        res['succ_msg']="Sensor binding Done and Application Scheduled!!"
        app_instance_id = res['AII']
        url_end_user = 'http://' + os.environ.get('request_manager_service_ip') + ':' + os.environ.get('request_manager_service_port')+'/app/' + app_instance_id + '/'
        # url_end_user = 'http://localhost:11000/'
        return render_template('sensor_form.html',succ_msg=res['succ_msg'],sensors=to_send,app_name=appName,url=url_end_user)






if __name__ == '__main__':
    app.run(debug=False, port="5000", host='0.0.0.0')