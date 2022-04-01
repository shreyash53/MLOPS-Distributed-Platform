import json
from kafka import KafkaConsumer
import requests

URL="http://127.0.0.1:8000"

listener = KafkaConsumer('notifications')
for msg in listener:
    j = json.loads(msg.value)
    r = requests.post(URL+'/notify', json={"recipient_id" : j['recipient_id'], "msg" : j['msg']})
    print(r)
    print(msg)