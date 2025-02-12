import pyrebase
import os,json
from dotenv import dotenv_values

secret=dotenv_values(".env")

fb_config = {
    "apiKey": secret["APIKEY"], #El [1:-2] es para borrar las comillas y el salto de linea
    "authDomain": f"{secret["PROJECT_ID"]}.firebaseapp.com",
    "databaseURL":f"https://{secret["PROJECT_ID"]}-default-rtdb.firebaseio.com",
    "projectId": f"{secret["PROJECT_ID"]}",
    "storageBucket": f"{secret["PROJECT_ID"]}.appspot.com",
    "serviceAccount":json.loads(secret["FIREBASE_CONFIG"])
}
print(secret)
fb=pyrebase.initialize_app(fb_config)
auth=fb.auth()
db=fb.database()
user={}