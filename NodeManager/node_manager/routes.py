from flask import Blueprint, request
from utilities.constants import GET, POST
from .controller import add_all_nodes

blueprint = Blueprint('Node', __name__, url_prefix='/node')

@blueprint.route('/add', methods = POST)
def addNode():
    nodes_data = request.get_json()
    return add_all_nodes(nodes_data)

# @blueprint.route('/plus', methods=POST)