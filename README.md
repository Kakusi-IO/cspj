# README

## 用docker-compose的开发流程

### 构建、运行
docker-compose up -d

### 接入shell
docker-compose exec web /bin/bash

### 查看log
docker-compose logs --tail=10

## MODELS



## URLS

- / 主页，对应hw.html，介绍网站功能
- list/ 任务列表，展示所有发布的任务，登录后自动跳转到这里
- signup/ 注册，提交注册的post请求之后会自动跳转到登录界面 （注册时会生成一条User和Profile）
- login/ 登录
- profile/ 个人中心，可以看到头像用户名等基本信息，还有若干任务列表
  - 自己发布的，发布待领取的任务列表
  - 自己发布的，有人提交测试样例答题结果，等待自己确认的任务列表
  - 自己发布的，确认被领取的，别人正在做的任务列表
  - 别人发布的，...
  - 以上用QuerySet的filter都可以找到，我已经定义好userid123列了
- upload/ 发布任务时用，暂时没想好内容
- 任务相关，从profile/的任务列表或者list/直接跳转
  - detail/ 任务详情页面（有不同的状态：已发布、已认领、已完成），可以领取任务
  - 答题页面（测试样例 和 正式完成）
  - 答题提交后返回list/
