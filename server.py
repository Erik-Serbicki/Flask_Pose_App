from flask import Flask, Response, render_template, request
from pose_detector import gen_frames
from threading import Thread

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')