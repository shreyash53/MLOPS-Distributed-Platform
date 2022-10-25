
from node_manager.model import RunningServices
from utilities.constants import GET, POST
from flask import request, Blueprint
from .controller import get_model_data, get_sensor_data
from node_manager.controller import get_node_by_id

blueprint = Blueprint('Request', __name__, url_prefix='/api')


@blueprint.route('/model/<modelId>', methods=POST)
def model_data(modelId):
    route = request.args.get('route')
    request_data = request.get_json()
    return get_model_data(modelId, request_data, route)

@blueprint.route('/sensor/<sensorId>', methods=GET)
def sensor_data(sensorId):
    print('api call')
    return get_sensor_data(sensorId)

#for testing
@blueprint.route('/add', methods=POST)
def addRunningService():
    try:
        data = request.get_json()
        node = get_node_by_id(data['node_id'])
        d = {
            "serviceId" : data['service_id'],
            "serviceType" : data['service_type'],
            "node" : node.to_dbref()
        }
        service_ = RunningServices(**d) 
        service_.save()
        return 'success'
    except Exception as e:
        print('service not added',e)
        return 'failure'