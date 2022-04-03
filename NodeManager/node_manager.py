from flask import Flask
from node_manager_config import DB_URI
from mongoengine.connection import connect

app = Flask(__name__)

app.config['SECRET_KEY'] = '10101010101010'

 
connect(db=DB_URI)
