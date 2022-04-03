from flask import Flask
import jsonify
import random
import json
import numpy as np
app = Flask(__name__)


def get_data():
    x=np.random.random((24,24))
    return x.tolist()


@app.route('/', methods=["POST"])
def hello_world():
    val = get_data()
    print(val)
    jsonString = json.dumps(val)
    return jsonString


if __name__ == '__main__':
	app.run(debug=True, port=5006)
