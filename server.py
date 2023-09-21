from flask import Flask, Response, render_template, request, make_response, jsonify
from pose_detector import *
from threading import Thread

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/image_pose")
def image_pose():
    response = make_response(img_pose())
    response.headers.set("Content-Type", "image/png")
    return response

app.run(host="0.0.0.0")