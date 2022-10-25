from flask import Flask, jsonify, request

import os
import dotenv
dotenv.load_dotenv() 
PORT = os.environ.get("SERVICE_PORT")
# Assuming : Model Class file is included in "dependencies"

import <fileName>
app = Flask(__name__)


# @app.route('/get_result', methods=['POST'])
# def get_result():
#     res = request.get_json()
#     return jsonify({"result":<fileName>.<predict_fun_name>(**res)})

# if __name__ == "__main__":
#     app.run(debug=False, port=PORT, host='0.0.0.0')
