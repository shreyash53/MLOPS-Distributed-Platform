from ast import comprehension
from ctypes import sizeof
import cv2
import threading
import flask
import json
import numpy as np
from time import sleep
import kafka
from json import dumps
# import matplotlib.pyplot as plt

frame = ""

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

produce = kafka.KafkaProducer(bootstrap_servers='52.140.63.83:9092',
                    value_serializer=lambda v: v.encode('utf-8'),
                    compression_type='gzip',
                    max_request_size=19048576,
                    # value_serializer=lambda v: dumps(v).encode('utf-8')
                    )
app = flask.Flask(__name__)
def capture():
    global frame
    cap = cv2.VideoCapture('dog_video/vid.mp4')
    frame = None
    while True:
        ret, frame = cap.read()
        # resize image
        frame = cv2.resize(frame, (1100,800), interpolation = cv2.INTER_AREA)
        print(frame.shape)
        # plt.imshow(resized)
        # plt.show()
        # cv2.imshow("he",resized)
        # cv2.waitKey(2)
        dmp = dumps(frame,cls=NumpyEncoder )
        # fuck = dumps(frame,cls=NumpyEncoder)
        print(len(dmp)/(1024*1024))
        print(dmp[:30])
        print("producing data")
        print(len(dmp))
        produce.send("dogsensor",dmp)
        print("sent")
        sleep(60)
        if ret == True:
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route("/getimage" , methods =["POST","GET"])
def fun():
    json_dump = json.dumps({"data" : frame}, cls=NumpyEncoder)
    return json_dump
if __name__ == "__main__":
    # t1 = threading.Thread(target = capture)
    # t1.start()
    capture()
    # app.run('0.0.0.0',debug=False, port=4999)
