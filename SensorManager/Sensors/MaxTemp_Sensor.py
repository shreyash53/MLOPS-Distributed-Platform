from flask import Flask
import jsonify
import random
import json

app = Flask(__name__)


def get_data():
    return round(random.uniform(25.0, 31.0),2)

@app.route('/', methods=["POST"])
def hello_world():
    val = get_data()
    print(val)
    jsonString = json.dumps(val)
    return jsonString


if __name__ == '__main__':
	app.run(debug=True, port=8007, host="0.0.0.0")
