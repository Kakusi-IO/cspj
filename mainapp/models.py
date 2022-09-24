from django.db import models
from .Task import Task, TextTask, AudioTask, ImgTask

# Create your models here.
class TasksModel(models.Model):
    size = models.IntegerField(default=0)