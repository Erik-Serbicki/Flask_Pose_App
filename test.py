import pyrebase

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

# set up storage
storage = firebase.storage()
imgPath = "assets/thrust1_pic.png"
storagePath = "images/thrust1_pic.png"

images = storage.child("images").list_files()
for i in images:
    print(storage.child(i.name).get_url(None))

#upload to storage
#storage.child("images/thrust1_pic.png").put(imgPath)

#download
# storage.child("images/thrust1_pic.png").download("assets/thrust2_pic.png")
