from kafka import KafkaProducer
import cv2
import sys
import time
import json
producer=KafkaProducer(bootstrap_servers="52.140.63.83:9092",api_version=(0,10,1))
image = cv2.imread("abc.jpg")
ret, buffer = cv2.imencode('.jpg', image)
print(len(
    buffer.tobytes()))
producer.send("imagekafka", buffer.tobytes())
time.sleep(15)