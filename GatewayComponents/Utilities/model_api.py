from flask import Flask, request
import pandas as pd
import pickle
import sys
from util.constants import *
# Assuming : Model Class file is included in "dependencies"
<other_dependencies>
app = Flask(__name__)


@app.route('/get_result', methods=['POST'])
def get_result():
    mdict = request.json()
    array = pd.DataFrame(mdict)

    pickle_file = open('<pickle_file_path>', 'rb')
    model = pickle.load(pickle_file)
    res = model.<preprocess_fun_name>(<preprocessing_para_name>)
    res = model.<predict_fun_name>(<predict_para_name>)
    res = model.<postprocess_fun_name>(<postprocessing_para_name>)
    pickle_file.close()
    return str(res)

if __name__ == "__main__":
    port_no = sys.argv[1]
    app.run(debug=False, port="5000", host='0.0.0.0')