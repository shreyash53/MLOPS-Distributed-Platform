
from utilities.constants import GET, POST
from flask import request, Blueprint
from .controller import get_model_data, get_sensor_data

blueprint = Blueprint('Request', __name__, url_prefix='/api')

@blueprint.route('/model/<modelId>', methods=POST)
def model_data(modelId):
    request_data = request.get_json()
    return get_model_data(modelId, request_data)

@blueprint.route('/sensor/<sensorId>', methods=GET)
def sensor_data(sensorId):
    return get_sensor_data(sensorId)