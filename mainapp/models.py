from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 描述分类任务的集合，是任务发布的最小单位
class TasksModel(models.Model):
    name = models.CharField(max_length=64, default='hogehoeg')
    description = models.CharField(max_length=256, default='hogehoge')
    size = models.IntegerField(default=0)
    reward = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

# 描述每条分类任务
class TaskModel(models.Model):
    tasks = models.ForeignKey(TasksModel, on_delete=models.CASCADE, null=True)
    # 0 文本 1 音频 2 图像 ...
    tasktype = models.IntegerField(default=0)
    # 描述选项，用特殊字符分割，暂定~
    choices = models.CharField(max_length=256, default='hogehoge')
    # 描述选项答案，二进制，低位表示前面的选项，支持多选
    answer = models.IntegerField(default=0)
    def __str__(self):
        return self.choices


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    point = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
