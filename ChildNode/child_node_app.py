from flask import Flask
from mongoengine.connection import connect
from child_node_config import DB_URI

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = '10101010101010'

connect(db=DB_URI)

 
