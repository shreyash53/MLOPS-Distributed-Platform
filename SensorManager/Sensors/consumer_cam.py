from filecmp import dircmp
from PIL import Image
from io import BytesIO
from kafka import KafkaConsumer
from flask import Flask,request,jsonify
import numpy as np
import json
import cv2
from time import sleep

while(1):
    consumer = KafkaConsumer("t_k1",bootstrap_servers=['52.140.63.83:9092'])
    for message in consumer:
        print("Message Recieved")
        # print(message.value)
        stream = BytesIO(message.value)
        # print("dict:\n",dict['b'])
        print("Stream:", type(stream.getvalue()))
        image = Image.open(stream).convert("RGB")
        frame = np.array(image)
        stream.close()
        image.show()
        image.save("result.jpg")
        # cv2.imwrite("result.jpg", frame)
    sleep(20)

    # image.show()
    # Converted numpy array to List to send it through JSOn
        # converting list to numpy array to show it in image form (Remember to keep dtype = uint8)
        # a = predict(dict_a['b'])
        # a = face_model.predict(dict_a['b'])
        # print("answer: ",a)
        # img =  np.array(dict_a['b'], dtype=np.uint8)
        # print(img.shape)
        # cv2.imwrite('color_img.jpg', img)
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        # return dict_a