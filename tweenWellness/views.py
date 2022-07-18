from distutils.command.config import config
from django.shortcuts import render
import pyrebase
from django.contrib import auth

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


def signIn(request):
    return render(request, "signIn.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "signIn.html", {"messg": message})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, 'welcome.html', {'e': email})


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render(request, 'signIn.html')


def addTips(request):

    return render(request, 'addTips.html')


def tips_add(request):

    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    tips = request.POST.get('tips')
    tips_image = request.POST.get('tips_image')
    url = request.POST.get('url')
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        print("info"+str(a))

        data = {
            "tips": tips,
            'tips_image': tips_image,
            'url':url
        }

        database.child('users').child(a).child('HTips').child(millis).set(data, idtoken)
            
        name = database.child('users').child(a).child(
            'details').child('name').get(idtoken).val()
        return render(request, 'welcome.html', {'e': name})
    except KeyError:
        message = "Oops! User have Logged Out. Please Sign In Again!"
        return render(request, "signIn.html", {"messg": message})

def updateTips(request):
    time = request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    placetips = database.child('users').child(a).child('HTips').child(time).child('tips').get().val()
    img_url = database.child('users').child(a).child('HTips').child(time).child('url').get().val()
    
    return render(request, 'updateTips.html', {'time': time, 'w': placetips, 'i': img_url})

def tips_update(request):
    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    tips = request.POST.get('tips')
    tips_image = request.POST.get('tips_image')
    url = request.POST.get('url')

    data = {
            "tips": tips,
            'tips_image': tips_image,
            'url':url
        }

    database.child('users').child(a).child('HTips').child(time).set(data, idtoken)

    return render(request,'welcome.html')


def tips_delete(request):
    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    
    tips = request.POST.get('tips')
    tips_image = request.POST.get('tips_image')
    url = request.POST.get('url')

    data = {
            "tips": tips,
            'tips_image': tips_image,
            'url':url
        }

    database.child('users').child(a).child('HTips').child(time).set(data, idtoken)

    return render(request,'welcome.html')

def checkTips(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestamps = database.child('users').child(
        a).child('HTips').shallow().get().val()
    lis_time = []
    for i in timestamps:

        lis_time.append(i)

    lis_time.sort(reverse=True)

    print(lis_time)
    tips = []

    for i in lis_time:

        tip = database.child('users').child(a).child('HTips').child(i).child('tips').get().val()
        tips.append(tip)
    print(tips)

    date = []
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    print(date)

    comb_lis = zip(lis_time, date, tips)
    name = database.child('users').child(a).child(
        'details').child('name').get().val()

    return render(request, 'checkTips.html', {'comb_lis': comb_lis, 'e': name})


def tips_check(request):

    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    tips = database.child('users').child(a).child('HTips').child(time).child('tips').get().val()
    tips_image = database.child('users').child(a).child('HTips').child(time).child('tips_image').get().val()
    img_url = database.child('users').child(a).child('HTips').child(time).child('url').get().val()
    print(img_url)

    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = database.child('users').child(a).child(
        'details').child('name').get().val()

    return render(request,'tips_check.html',{'w':tips,'p':tips_image,'d':dat,'e':name,'i':img_url})


#Temp
def index(request):
    htips_title = database.child('HTips').child(
        '01').child('Addedby').get().val()
    channel_type = database.child('Data').child('Type').get().val()
    subscribers = database.child('Data').child('Subscribers').get().val()

    return render(request, 'tweenWellness/index.html', {
        "htips_title": htips_title,
        "channel_type": channel_type,
        "subscribers": subscribers
    })
