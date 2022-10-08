from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 描述分类任务的集合，是任务发布的最小单位
class TasksModel(models.Model):
    key = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, default='hogehoeg')
    description = models.CharField(max_length=256, default='hogehoge')
    reward = models.IntegerField(default=0)
    userid1 = models.IntegerField(default=0) # 发布者id
    userid2 = models.IntegerField(null=True) # 领取者id
    userid3 = models.IntegerField(null=True)  # 请求测试者id
    status = models.IntegerField(default=0) # 0 未领取 1 测试结果未确认 2 进行中 3 已完成
    
    def __str__(self):
        return self.name

# 描述每条分类任务
class TaskModel(models.Model):

    belong = models.IntegerField(default=0)
    tasktype = models.IntegerField(default=0) # 0 文本 1 音频 2 图像 ...
    content = models.CharField(max_length=256, default='hogehoge')
    answer = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Profile(models.Model):
    key = models.IntegerField(primary_key=True, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
