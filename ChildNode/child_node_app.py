from flask import Flask
from mongoengine.connection import connect
from child_node_config import DB_URI, database_name, DB_USER_NAME, DB_PASSwORD

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = '10101010101010'

connect(db=database_name, username=DB_USER_NAME, password=DB_PASSwORD, host=DB_URI)

 
