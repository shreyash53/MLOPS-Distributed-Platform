from flask import Flask
import random
import json 

app = Flask(__name__)

def get_data():
    randomlist=[]
    for i in range(7):
        randomlist.append(round(random.uniform(30.0, 38.0),1))
    return randomlist

@app.route('/',methods=["POST"])
def hello_world():
    val = get_data()
    print(val)
    jsonString = json.dumps(val)
    return jsonString

if __name__ == '__main__':
	app.run(debug=True,port=5000)
