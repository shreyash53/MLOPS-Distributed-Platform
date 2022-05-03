from flask import Flask, jsonify, request

import model

app = Flask(__name__)


@app.route('/get_result', methods=['POST'])
def result():
    print('api hit')
    res = request.get_json()
    return jsonify({"result":model.predict(**res)})

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=5000)
from flask import Flask, jsonify, request

import os
import dotenv
dotenv.load_dotenv() 
PORT = os.environ.get("SERVICE_PORT")
# Assuming : Model Class file is included in "dependencies"

import model
app = Flask(__name__)


# @app.route('/get_result', methods=['POST'])
# def get_result():
#     res = request.get_json()
#     return jsonify({"result":model.<predict_fun_name>(**res)})

# if __name__ == "__main__":
#     app.run(debug=False, port=PORT, host='0.0.0.0')@app.route('/get_result>', methods=['POST','GET'])
def predict():
	res = request.get_json()
	return jsonify({'result':model.predict(**res)})
@app.route('/get_test>', methods=['POST','GET'])
def test():
	res = request.get_json()
	return jsonify({'result':model.test(**res)})
if __name__ == "__main__":
	app.run(debug=False, port=PORT, host="0.0.0.0")"