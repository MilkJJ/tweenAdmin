from distutils.command.config import config
from django.shortcuts import render
import pyrebase

config = {
  "apiKey": "AIzaSyD-W8-PnNuX4TxxcAaxMtYFKbhIh3mIb5A",
  "authDomain": "tween-wellness-app-6dc50.firebaseapp.com",
  "databaseURL": "https://tween-wellness-app-6dc50-default-rtdb.firebaseio.com",
  "projectId": "tween-wellness-app-6dc50",
  "storageBucket": "tween-wellness-app-6dc50.appspot.com",
  "messagingSenderId": "569008204612",
  "appId": "1:569008204612:web:f3f09acb767c78b1294511",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.
def index(request):
    channel_name = database.child('Data').child('Name').get().val()
    channel_type = database.child('Data').child('Type').get().val()
    subscribers = database.child('Data').child('Subscribers').get().val()

    return render(request, 'tweenWellness/index.html', {
    "channel_name": channel_name,
    "channel_type": channel_type,
    "subscribers": subscribers
    })