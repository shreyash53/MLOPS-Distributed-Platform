from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from Authenticate import *
#import mongoengine as db
from AppUpload.App_Upload import *
from ModelUpload.Model_Upload import *
from Utilities.dbconfig import *
app = Flask(__name__)
db=mongodb()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Actor.db'
#database_name = 'requestmanager_db'
#DB_URI =  'mongodb+srv://kamal:kamal123@cluster0.lzygp.mongodb.net/{}?retryWrites=true&w=majority'.format(database_name)
app.config['SECRET_KEY'] = 'root'

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if  not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            print( data['username'])
            current_user = Actor.objects(username = data['username']).first()
        except:
            return jsonify({'message':'Token is invalid!!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated



@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/login_')
def login_render():
    return render_template('login.html')

@app.route('/signup',methods=["POST"])
def signup_req():
    resp = signup({  'username':request.form['username']  ,  'password':request.form['password']  ,  'role':request.form['role']  })
    if 'succ_msg' in resp:
        return render_template('signup.html',succ_msg=resp['succ_msg'])
    else:
        return render_template('signup.html',err_msg=resp['err_msg'])

@app.route('/login',methods=["POST"])
def login_req():
    return jsonify(login(request))

@app.route('/app_developer',methods=["POST"])
# @token_required
def app_developer_view():
# def app_developer_view(current_user):
    # if current_user.role != 'app_developer':
    #     return 'Invalid Request(Role Mismatch)'
    sensor_details = [('T1','DT1'),('T2','DT2'),('T1','DT2')]
    model_details = ['m1','m2','m3']
    return render_template('app_developer.html',sensor_details=sensor_details,model_details=model_details)

@app.route('/platform_admin',methods=["POST"])
@token_required
def platform_admin_view(current_user):
    if current_user.role != 'platform_admin':
        return 'Invalid Request(Role Mismatch)'
    sensor_details = [('T1','DT1'),('T2','DT2'),('T1','DT2')]
    model_details = ['m1','m2','m3']
    return render_template('platform_admin.html',sensor_details=sensor_details,model_details=model_details)

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
    sensor_details = [('T1','DT1'),('T2','DT2'),('T1','DT2')]
    model_details = ['m1','m2','m3']
    if 'err_msg' in resp:
        return render_template('platform_admin.html',sensor_details=sensor_details,model_details=model_details,err_msg=resp['err_msg'])
    elif 'succ_msg' in resp:
        return render_template('platform_admin.html',sensor_details=sensor_details,model_details=model_details,succ_msg=resp['succ_msg'])
    return render_template('platform_admin.html',sensor_details=sensor_details,model_details=model_details)

@app.route('/data_scientist/upload_model',methods=['POST'])
@token_required
def upload_model(current_user):
    if current_user.role != 'data_scientist':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401    
    return jsonify(upload_model_file(request))

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
    return jsonify({"message":"Able to access because token verified", "user":current_user.username , "role":current_user.role}), 200

@app.route('/platform_admin/add_node',methods=['POST'])
@token_required
def add_node(current_user):
    if current_user.role != 'platform_admin':
        return jsonify({"message":"Invalid Role("+current_user.role+") for user:"+current_user.username, "user":current_user.username , "role":current_user.role}), 401    
    return jsonify({"message":"Able to access because token verified", "user":current_user.username , "role":current_user.role}), 200

if __name__ == '__main__':
    app.run(debug=True)