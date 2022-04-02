from crypt import methods
from flask import Flask, request, render_template
from dbconfig import *
import requests

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = '8008'

db = mongodb()



@app.route("/get_logs", methods=['POST'])
def home():
    service_name = request.json['service_name']
    logs = Logs.objects(service_name=service_name)
    return logs


if __name__ == "__main__":
    app.run(host=HOST,port=PORT, debug=True)
