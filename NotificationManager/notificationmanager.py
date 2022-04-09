from threading import Thread
from flask import Flask, request
from dbconfig import *
from dotenv import load_dotenv
from kafka import KafkaConsumer
import json
import requests


from constant import BOOTSTRAP_SERVERS


load_dotenv('.env')
app = Flask(__name__)

db = mongodb()


class Actor(db.Document):
    _id = db.StringField(required=True, primary_key=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True)

    meta = {'db_alias': 'user_db'}


class Notification(db.Document):
    recipient_id = db.ReferenceField(Actor)
    msg = db.StringField(min_length=1, required=True)
    is_read = db.BooleanField(required=True)

    meta = {'db_alias': 'notifs_db'}


@app.route('/fetch', methods=['GET'])
def get_notifications():
    recipient_id = request.json['recipient_id']
    if recipient_id is None or '':
        return "No user ID provided."
    else:
        notifs = Notification.objects(
            recipient_id=recipient_id).order_by("-_id")
        return notifs.to_json()


@app.route('/notify', methods=['POST'])
def send_notification():
    if 'recipient_id' not in request.json:
        raise Exception("No recipient given")
    if 'msg' not in request.json:
        raise Exception("Empty message!")
    else:
        rec_id = request.json['recipient_id']
        msg = request.json['msg']

        try:
            valid = False if Actor.objects(
                _id=rec_id).first() is None else True

            if not valid:
                raise Exception("Recipient does not exist!")
            Notification(recipient_id=rec_id, msg=msg, is_read=False).save()

        except Exception as e:
            raise Exception("Error while sending notification : " + str(e))

        return "Notification Sent!"

URL="http://0.0.0.0:8000"


def listen_for_notifs():
    listener = KafkaConsumer('notifications', bootstrap_servers=BOOTSTRAP_SERVERS)
    for msg in listener:
        try:
            j = json.loads(msg.value.decode('UTF-8'))
            print(j)
            r = requests.post(URL+'/notify', json={"recipient_id" : j['recipient_id'], "msg" : j['msg']})
            print(r)
        except json.JSONDecodeError as e:
            print(str(e) + " in " + msg.value.decode('UTF-8'))
        except Exception as e:
            print("Error : " + str(e))


if __name__ == "__main__":
    listener = Thread(target=listen_for_notifs)
    listener.start()
    app.run(debug=False, port="5000", host='0.0.0.0')

