from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

from sql_app.crud import *

def listfunc(request):
    # TODO: 列出所有任务，支持按状态筛选，按时间排序

    objs = {

    }
    return render(request, 'list.html', objs)


def profilefunc(request):
    # TODO: 用户详细信息，有修改头像、密码的入口
    # 列出属于该用户的任务（发布和认领的） get_task_by_user
    user = request.user
    objs = {
        "user": user,

    }
    return render(request, 'profile.html', objs)


def hwfunc(request):
    return render(request, 'hw.html', {})


def signupfunc(request):
    # TODO: 收集email和电话号码（email要验证）
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
            create_profile(user_id=user.id)
        except Exception as e:
            # messages.error(request, 'Duplicated user name.')
            message = e
        finally:
            return render(request, "signup.html", {"message": message})

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
    # TODO: logout页面
    logout(request)
    return redirect('login')


def uploadfunc(request):
    # TODO: 上传文件
    if request.method == 'POST':
        pass
    return render(request, 'upload.html', {})


def detailfunc(request, pk):
    # TODO: 任务详情
    objs = {

    }
    return render(request, 'detail.html', objs)

def upload_file(request):
    if request.method == 'POST':
        # TODO: 上传任务文件
            return render(request, "upload.html", {"message": "OK"})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
