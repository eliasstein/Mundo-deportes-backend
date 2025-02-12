import pyrebase
import os

fb_config = {
    "apiKey": os.getenv("APIKEY"), #El [1:-2] es para borrar las comillas y el salto de linea
    "authDomain": f"{os.getenv("PROJECT_ID")}.firebaseapp.com",
    "databaseURL":f"https://{os.getenv("PROJECT_ID")}-default-rtdb.firebaseio.com",
    "projectId": f"{os.getenv("PROJECT_ID")}",
    "storageBucket": f"{os.getenv("PROJECT_ID")}.appspot.com",
    "serviceAccount":"firebase.json"
}
fb=pyrebase.initialize_app(fb_config)
auth=fb.auth()
db=fb.database()
user={}