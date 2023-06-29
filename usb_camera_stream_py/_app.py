import base64
import threading

import cv2
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

camera = cv2.VideoCapture(0)


def cap_cam():
    while True:
        socketio.sleep(0.01)
        success, frame = camera.read()
        if not success:
            break
        else:
            _, jpeg = cv2.imencode(".jpg", frame)
            base64_image = base64.b64encode(jpeg).decode("utf-8")
            socketio.emit("video_frame", base64_image)


@app.route("/")
def index():
    return render_template("_index.html")


@socketio.on("connect")
def connect():
    socketio.emit("to_client", {"from": "server"})
    socketio.start_background_task(cap_cam)


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=4000)
