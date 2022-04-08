from re import X
from flask import Flask
import jsonify
import random
import json
import sys
from new_con import *

app = Flask(__name__)


# def get_data():
#     return (round(random.uniform(60.0, 70.0), 2))

@app.route('/testAPI', methods=["POST"])
def hello_world():
    x= get_value_from_topic()
    print(type(x))
    return x

if __name__ == '__main__':
	app.run(debug=True, port=8008)
