from flask import Flask
from node_manager_config import DB_URI
from mongoengine.connection import connect
from request_interface.routes import blueprint as request_interface_blueprint
app = Flask(__name__)

app.config['SECRET_KEY'] = '10101010101010'
 
connect(db=DB_URI)

app.register_blueprint(request_interface_blueprint)