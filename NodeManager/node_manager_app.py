from flask import Flask
from node_manager_config import DB_URI, DB_USER_NAME, DB_PASSwORD, database_name
from mongoengine import connect
from request_interface.routes import blueprint as request_interface_blueprint
from node_manager.routes import blueprint as node_manager_blueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = '10101010101010'

connect(db=database_name, username=DB_USER_NAME, password=DB_PASSwORD, host=DB_URI)

app.register_blueprint(request_interface_blueprint)
app.register_blueprint(node_manager_blueprint)