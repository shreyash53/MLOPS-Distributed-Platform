from flask import Flask, request
import pandas as pd
import pickle
import sys
from util.constants import *
# Assuming : Model Class file is included in "dependencies"

dep1
dep2
dep3
dep4
dep5
dep6
dep7
dep8
app = Flask(__name__)


@app.route('/get_result', methods=['POST'])
def get_result():
    mdict = request.json
    array = pd.DataFrame(mdict)

    pickle_file = open('model_demo_pickle.pkl', 'rb')
    model = pickle.load(pickle_file)
    res = model.preprocessing(array)
    res = model.predict(array)
    res = model.postprocessing(array)
    pickle_file.close()
    return str(res)

if __name__ == "__main__":
    port_no = sys.argv[1]
    app.run(port=port_no)