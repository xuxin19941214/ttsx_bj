#coding=utf-8
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)#sha1加密
    umail=models.CharField(max_length=30)
    uconsignee=models.CharField(default='',max_length=20)#收货人
    uaddress=models.CharField(default='',max_length=100)
    ucode=models.CharField(default='',max_length=6)
    uphone=models.CharField(default='',max_length=11)