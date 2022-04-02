import datetime
import jwt
from functools import wraps

from matplotlib import use
from RequestManager import db,app
from Utilities.models import Actor
from flask import jsonify,request

def signup(req):
    # req = req.get_json()    
    username = req['username']
    password = req['password']
    role = req['role']
    actor = Actor.objects(username = username).count()
    print("Number of actors in actor db:",actor)
    if actor > 0:
        return {'err_msg':'User already exist'}
    actor = Actor(username = username , password = password , role = role)
    actor.save()

    return {'succ_msg':'Successfully added'}

def login(req):
    req = req.get_json()
    # print("REQUEST IN AUTHENTICATOR:",req)
    username = req['username']
    password = req['password']
    role = req['role']
    # print(username,password,role)
    if Actor.objects(username = username).count() == 0:
        return {'err_msg':'User not found'}
    if Actor.objects(username = username , role = role).count() == 0:
        return {'err_msg':'User with this role not found'}
    if Actor.objects(username = username,password = password , role = role).count() == 0:
        return {'err_msg':'Incorrect password'}
    token = encode_auth_token(username,role).decode('utf-8')
    
    return {'token':token,'succ_msg':'Authentication Successfull','username':username,'role':role}

def encode_auth_token(username,role):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
            'iat': datetime.datetime.utcnow(),
            'username': username,
            'role':role
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY')
        )
    except Exception as e:
        return e