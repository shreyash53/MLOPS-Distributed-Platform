import cv2
from time import sleep
from kafka import KafkaProducer
from flask import Flask
import sys
import numpy as np
app = Flask(__name__)

kafka_server = sys.argv[1]
topic_name = sys.argv[2]
while(1):
  producer = KafkaProducer(bootstrap_servers=[kafka_server])
  image = cv2.imread("bill.jpg")
  ret, buffer = cv2.imencode('.jpg', image)
  print(buffer.shape)
  a = buffer.tobytes()
  producer.send(topic_name, buffer.tobytes())
  data = np.frombuffer(a, dtype=buffer.dtype)
  print(data.shape)
  sleep(20)

if __name__ == '__main__':
	app.run(debug=True, port=5006)
