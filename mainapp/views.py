from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth.models import User
# from django.contrib import messages
# from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, logout, login
# from django.views.generic import ListView
from .forms import UploadFileForm

import mysql.connector
from .mydb import db


def listfunc(request):
    db.connect()
    mycursor = db.mydb.cursor()
    mycursor.execute("select * from task order by create_at desc")
    tasks = mycursor.fetchall()

    objs = {
        "tasks": [dict(zip(
            ("id", "owner_id", "name", "reward", "create_at", "update_at"),
            t
        )) for t in tasks]
    }
    return render(request, 'list.html', objs)


def profilefunc(request):
    user = request.user
    # print(user.id)
    db.connect()
    mycursor = db.mydb.cursor()
    mycursor.execute(
        "select * from profile where user_id = {}".format(user.id))
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
        "myTasks": [dict(zip(
            ("id", "owner_id", "name", "reward", "create_at", "update_at"),
            t
        )) for t in myTasks]
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

    db.connect()
    mycursor = db.mydb.cursor()
    mycursor.execute("select * from task where id = {}".format(pk))
    task = mycursor.fetchone()

    mycursor = db.mydb.cursor()
    mycursor.execute("select * from single_task where task_id = {}".format(pk))
    single_tasks = mycursor.fetchall()

    objs = {
        "task": dict(zip(
            ("id", "owner_id", "name", "reward", "create_at", "update_at"),
            task
        )),
        "single_tasks": [dict(zip(
            ("id", "task_id", "type_id", "create_at", "update_at"),
            st
        )) for st in single_tasks]
    }
    return render(request, 'detail.html', objs)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print("checking...")
        # if form.is_valid():
        if True:
            print("valid")
            handle_uploaded_file(request.FILES['file'])
            return render(request, "upload.html", {"message": "OK"})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    print("handle_upload_file")
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            print("saving...")
            destination.write(chunk)