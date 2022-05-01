import cv2
import threading
import flask
import json
import numpy as np
from time import sleep

frame = ""

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

app = flask.Flask(__name__)
def capture():
    global frame
    cap = cv2.VideoCapture('dog_video/vid.mp4')
    frame = None
    while True:
        ret, frame = cap.read()
        sleep(0.2)
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
    t1 = threading.Thread(target = capture)
    t1.start()
    app.run('0.0.0.0',debug=True)
