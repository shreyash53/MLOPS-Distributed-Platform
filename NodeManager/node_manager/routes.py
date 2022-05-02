from flask import Blueprint, request
from utilities.constants import GET, POST
from .controller import add_all_nodes, get_node_performance_data, get_node_list

blueprint = Blueprint('Node', __name__, url_prefix='/node')

@blueprint.route('/add', methods = POST)
def addNode():
    nodes_data = request.get_json()
    return add_all_nodes(nodes_data)


@blueprint.route('/get_node', methods = GET)
def getNodeList():
    return get_node_list()


@blueprint.route('/get_usage', methods = GET)
def getPerformanceData():
    return get_node_performance_data()

# @blueprint.route('/plus', methods=POST)