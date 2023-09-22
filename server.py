from flask import Flask, Response, render_template, request, make_response, jsonify, redirect, url_for
from pose_detector import *
import pyrebase
import tempfile
import os
import time

firebaseConfig = {"apiKey": "AIzaSyDlfb4ifsyyf4q92AidCqS4R-7_RtcfcaI",
  "authDomain": "hema-ai.firebaseapp.com",
  "projectId": "hema-ai",
  "storageBucket": "hema-ai.appspot.com",
  "messagingSenderId": "647236692047",
  "appId": "1:647236692047:web:b91bd96b7568ee01c7223a",
  "measurementId": "G-5DCJR1PHVN",
  "databaseURL":"",
  "serviceAccount":"C://Users/eriks/Documents/FirebaseAuth/hema-ai-firebase-admin.json"}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

uploadVidPath = "videos"

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

@app.route("/success", methods = ["POST"])
def success():
    if request.method=="POST":
        f = request.files["file"]
        temp = tempfile.NamedTemporaryFile(delete=False)
        f.save(temp.name)
        storage.child(f"{uploadVidPath}/{f.filename}").put(temp.name)
        process_video(f.filename)
        return render_template("uploaded.html", name=f.filename) 

@app.route("/display/<filename>")
def display_video(filename):
    pass


app.run(host="0.0.0.0")