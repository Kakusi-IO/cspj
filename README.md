# README

## 用docker-compose的开发流程

### 构建、运行
docker-compose up -d

### 接入shell
docker-compose exec web /bin/bash

### 查看log
docker-compose logs --tail=10

## NOTICE

直接运行`py sql_app/test.py`测试和运行`docker-compose`部署时，`sql_app`目录下的**同目录**import的写法不一样

直接运行py：`from models import *, from database import Base, SessionLocal`

docker部署：`from .models import *, from .database import Base, SessionLocal`

记得改，不然会报错

## API

todo

## URLS

- / 主页，对应hw.html，介绍网站功能
- list/ 任务列表，展示所有发布的任务
- signup/ 注册，提交注册的post请求之后会自动跳转到登录界面 （注册时会生成一条User和Profile）
- login/ 登录
- profile/ 个人中心
  - 以上用QuerySet的filter都可以找到，我已经定义好userid123列了
- upload/ 发布任务用

## 其他

在整体流程控制上，我们认为发布者是可信的，领取者是不可信的。领取者可能领取任务之后一直不做 or 乱做，发布者有权拒绝领取者的提交或者在用户提交之前终止任务，将任务回溯到新发布的状态。
