### Pose detection with mediapipe and cv2 - Erik Serbicki 7/22/2023

# Import dependencies
import cv2
import mediapipe as mp
import numpy as np
import time

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

