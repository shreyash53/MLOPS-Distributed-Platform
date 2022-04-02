from crypt import methods
from flask import Flask, request, jsonify, make_response,render_template


app = Flask(__name__)

@app.route('/sensor_validate', methods=["POST"])
def sensor_validate():
    sensor_data = request.get_json()
    for i in sensor_data['details']:
        if(i['sensortype']=='camera' or i['sensortype']=='microphone'):
            pass
        else:
            return {"msg":"error","status":0,"sensorid":i['sensorid']}
    return {"msg":"Success","status":1}

if __name__ == "__main__":
    app.run(port=9000,debug=True)

