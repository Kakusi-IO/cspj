from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth.models import User
# from django.contrib import messages
# from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, logout, login
# from django.views.generic import ListView

import mysql.connector
from .mydb import db


def listfunc(request):
    objs = {

    }
    return render(request, 'list.html', objs)

def profilefunc(request):
    user = request.user
    # print(user.id)
    db.connect()
    mycursor = db.mydb.cursor()
    mycursor.execute("select * from profile where user_id = {}".format(user.id))
    profile = mycursor.fetchone()

    mycursor = db.mydb.cursor()
    mycursor.execute("select * from task where owner_id = {}".format(user.id))
    myTasks = mycursor.fetchall()


    objs = {
        "user": user,
        "profile": dict(zip(
            ("id", "user_id", "points", "tel", "create_at", "update_at"), 
            profile
        )),
        "myTasks": myTasks
    }
    return render(request, 'profile.html', objs)


def hwfunc(request):
    return render(request, 'hw.html', {})


def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if not password == password2:
            return render(request, 'signup.html', {'message': 'Passwords of 2 input not match.'})
        message = "OK, Please log in."
        try:
            user = User.objects.create_user(
                username=username, password=password)
            db.connect()
            mycursor = db.mydb.cursor()
            sql = "INSERT INTO profile (user_id) VALUES ({})".format(user.id)
            # val = (user.id, )
            mycursor.execute(sql)
            db.mydb.commit()
        except Exception as e:
            # messages.error(request, 'Duplicated user name.')
            message = e
        finally:
            return render(request, "signup.html", {"message": message})

    return render(request, 'signup.html', {})


def loginfunc(request):
    # print(request.method)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            print('Not logged in')
            return render(request, 'login.html', {'message': 'Wrong username or password.'})
    return render(request, 'login.html', {})


def logoutfunc(request):
    logout(request)
    return redirect('login')


def uploadfunc(request):
    if request.method == 'POST':
        pass
    return render(request, 'upload.html', {})


def testfunc(request):
    objs = {

    }
    return render(request, 'test.html', objs)


def detailfunc(request, pk):
    objs = {

    }
    return render(request, 'detail.html', objs)
