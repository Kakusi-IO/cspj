from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
import requests
from os.path import join
import json

BASE_URL = 'http://0.0.0.0/api/'

def listfunc(request):
    print(BASE_URL)
    tasks = requests.get(join(BASE_URL, 'task/all'))
    obj = {
        'tasks': tasks.json()
    }
    return render(request, 'list.html', obj)

def detailfunc(request, pk):
    task = requests.get(join(BASE_URL, 'task'), params={'task_id': pk})
    single_tasks = requests.get(join(BASE_URL, 'task/single'), params={'task_id': pk})
    objs = {
        'task': task.json(),
        'single_tasks': single_tasks.json()
    }
    return render(request, 'detail.html', objs)

def profilefunc(request):
    user = request.user
    profile = requests.get(join(BASE_URL, 'user/profile'), params={'user_id': user.id})
    myTasks = requests.get(join(BASE_URL, 'user/tasks'), params={'owner_id': user.id})
    objs = {
        "user": user,
        'profile': profile.json(),
        'myTasks': myTasks.json()
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
        data = {
            'username': username, 'password': password
        }
        res = requests.post(join(BASE_URL, 'user/create'), data=json.dumps(data))
        return render(request, "signup.html", {'message': res.status_code})
    return render(request, 'signup.html', {})

def loginfunc(request):
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
    return render(request, 'upload.html', {})

def createtaskfunc(request):
    if request.method == 'POST':
        user = request.user
        taskname = request.POST['taskname']
        reward = request.POST['reward']
        typeno = request.POST['typeno']
        jsonfile = request.FILES['jsonfile']
        data = {'name': taskname, 'reward': reward, 'typeno': typeno, 'owner_id': user.id}
        res = requests.post(join(BASE_URL, 'task/create'), data=json.dumps(data))
        res = res.content.decode('utf-8')
        ress = requests.post(join(BASE_URL, 'task/single/upload'), params=json.loads(res), files={'file': jsonfile})
        print(ress.__dict__)
        # 422, 文件没传上
    return render(request, 'createtask.html', {})
