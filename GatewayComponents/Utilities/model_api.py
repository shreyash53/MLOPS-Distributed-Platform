from flask import Flask, jsonify, request
import sys
from util.constants import *
import os
import dotenv
dotenv.load_dotenv() 
PORT = os.environ.get("SERVICE_PORT")
# Assuming : Model Class file is included in "dependencies"
<other_dependencies>
app = Flask(__name__)


@app.route('/get_result', methods=['POST'])
def get_result():
    mdict = request.json()
    res = request.get_json()
    return jsonify({"result":model.'<predict_fun_name>'(**res)})
    # array = pd.DataFrame(mdict)

    # pickle_file = open('<pickle_file_path>', 'rb')
    # model = pickle.load(pickle_file)
    # res = model.<preprocess_fun_name>(<preprocessing_para_name>)
    # res = model.<predict_fun_name>(<predict_para_name>)
    # res = model.<postprocess_fun_name>(<postprocessing_para_name>)
    # pickle_file.close()
    # return str(res)

if __name__ == "__main__":
    app.run(debug=False, port=PORT, host='0.0.0.0')