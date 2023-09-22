### Pose detection with mediapipe and cv2 - Erik Serbicki 7/22/2023

# Import dependencies
import cv2
import mediapipe as mp
import numpy as np
import time
import pyrebase
import tempfile

# Set up firebase config
firebaseConfig = {"apiKey": "AIzaSyDlfb4ifsyyf4q92AidCqS4R-7_RtcfcaI",
  "authDomain": "hema-ai.firebaseapp.com",
  "projectId": "hema-ai",
  "storageBucket": "hema-ai.appspot.com",
  "messagingSenderId": "647236692047",
  "appId": "1:647236692047:web:b91bd96b7568ee01c7223a",
  "measurementId": "G-5DCJR1PHVN",
  "databaseURL":"",
  "serviceAccount":"C://Users/eriks/Documents/FirebaseAuth/hema-ai-firebase-admin.json"}

# Initialize Firebase and cloud storage
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

# Set path within storage
uploadVidPath = "videos"
proccessedVidPath = "processed"

# Set up mediapipe drawing (for display) and pose (for calculation)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Create colors (BGR)
lightblue = (220, 163 ,33)
bluegreen = (121, 207, 29)



def record(out):
    global rec_frame
    while(True):
        time.sleep(0.05)
        out.write(rec_frame)

# Create cv2 video feed with webcam
def gen_frames():
    cap = cv2.VideoCapture("assets/thrust1.mp4")
    # set up mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2) as pose:
        global out, capture, rec_frame
        while True:
            success, frame = cap.read()

            if success:

                # Recolor iamge to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmarks
                except:
                    pass

                # Display lines on image
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=lightblue, thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=bluegreen, thickness=2, circle_radius=2)
                                        )

                try:
                    ret, buffer = cv2.imencode('.png', cv2.flip(image, 1))
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass

            else: 
                pass

# Create pose for one image
def img_pose():
    cap = cv2.VideoCapture("assets/thrust1.mp4")  
    frames = []
    i = 0
    while(cap.isOpened()):
        ret, image = cap.read()
        if ret == False:
            break
        with mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2) as pose:
            results = pose.process(image)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=lightblue, thickness=2, circle_radius=2),
                                            mp_drawing.DrawingSpec(color=bluegreen, thickness=2, circle_radius=2)
                                            )
            ret, buffer = cv2.imencode('.png', cv2.flip(image,1))
            frame = buffer.tobytes()
            frames.append(frame)
        i += 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    cap.release()
    return frames[0]   

# Process a video from Firebase
def process_video(path):

    # Create temporary file to store video from firebase
    temp_download = tempfile.NamedTemporaryFile(delete=False)

    # Create temporary file to store video output before saving to firebase
    temp_upload = tempfile.NamedTemporaryFile(delete=False)

    # Download the firebase video and store it in the temporary file
    storage.child(f"{uploadVidPath}/{path}").download(path=tempfile.gettempdir(), filename=temp_download.name)

    # Create cv2 capture object from the downloaded file
    cap = cv2.VideoCapture(temp_download.name)

    # Get video properties to use for videowriter output
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(filename=temp_upload.name, fourcc=fourcc, fps=fps, frameSize=size)


    with mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2) as pose:
        while True:
            success, frame = cap.read()
            if success:
                # Recolor iamge to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmarks
                except:
                    pass

                # Display lines on image
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=lightblue, thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=bluegreen, thickness=2, circle_radius=2)
                                        )
                out.write(image)
            else:
                break
                  
    storage.child(f"{proccessedVidPath}/{path}").put(temp_upload.name)
