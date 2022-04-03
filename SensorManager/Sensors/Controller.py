from flask import Flask, request
import jsonify
import random
import json

app = Flask(__name__)


# def get_data():
#     randomlist = []
#     for i in range(7):
#         a = random.uniform(13.0, 16.0)
#         randomlist.append(round(a, 1))
#     return randomlist


@app.route('/', methods=["POST"])
def hello_world():
    request_data= request.json
    print(request_data)
    return "Successful"
    # val = get_data()
    # print(val)
    # jsonString = json.dumps(val)
    # return jsonString


if __name__ == '__main__':
	app.run(debug=True, port=5005)
