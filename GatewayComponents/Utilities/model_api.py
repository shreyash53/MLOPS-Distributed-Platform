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
    mdict = request.json
    array = pd.DataFrame(mdict)

    pickle_file = open('<pickle_file_path>', 'rb')
    model = pickle.load(pickle_file)
    res = model.<preprocess_fun_name>(array)
    res = model.<predict_fun_name>(array)
    res = model.<postprocess_fun_name>(array)
    pickle_file.close()
    return str(res)

if __name__ == "__main__":
    port_no = sys.argv[1]
    app.run(port=port_no)