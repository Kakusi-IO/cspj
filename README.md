# README

## 用docker-compose的开发流程

### 构建、运行
docker-compose up -d

### 接入shell
docker-compose exec web /bin/bash

### 查看log
docker-compose logs --tail=10

## MODELS

- TasksModel 描述数据集，是发布任务的单位
- TaskModel 描述单条分类任务，包括类型（图片/文本/音频），题干，选项（不知道正确选项）
- User 是django auth模块提供的用户类型，有基本的信息：用户名，密码，邮箱
- Profile 是扩展的用户数据，和User表的每条数据是一一对应关系，保存了该用户的头像图片和点数

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
  - 我需要先研究一下sql的用法再确认一下会传什么类型的参数给html
- upload/ 发布任务时用，暂时没想好内容
- 任务相关，从profile/的任务列表或者list/直接跳转
  - 任务详情页面（有不同的状态：已发布、已认领、已完成）
  - 领取任务页面
  - 答题页面（测试样例 和 正式完成）
  - 答题提交后返回list/
