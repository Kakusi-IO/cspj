from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, logout
# from django.views.generic import ListView
from .models import *

def listfunc(request):
    objs = {
        'me': request.user,
        't1': TasksModel.objects.all(),
        't2': TaskModel.objects.all(),
        't3': TaskModel.objects.filter(belong = 1),
    }
    return render(request, 'list.html', objs)

def profilefunc(request):
    user = request.user
    pf = get_object_or_404(Profile, user=user)
    t1 = TasksModel.objects.filter(userid1=pf.key) # 我发布的任务
    objs = {
        'me': user,
        'pf': pf,
        't1': t1,
        # 't1': 
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
        try:
            user = User.objects.create_user(username=username, password=password)
            return redirect('list')
        except IntegrityError:
            # messages.error(request, 'Duplicated user name.')
            return render(request, 'signup.html', {'message': 'Duplicated username.'})
    return render(request, 'signup.html', {})

def loginfunc(request):
    # print(request.method)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('redirect to list')
            return redirect('list')
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
        't1': TasksModel.objects.all(),
        't2': TaskModel.objects.all(),
        't3': TaskModel.objects.filter(belong = 1),
    }
    return render(request, 'test.html', objs)

def detailfunc(request, pk):
    objs = {
        't1': get_object_or_404(TasksModel, pk=pk),
        't2': TaskModel.objects.filter(belong=pk),
    }
    return render(request, 'detail.html', objs)