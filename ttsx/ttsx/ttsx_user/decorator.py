#coding=utf-8
from django.shortcuts import redirect
def user_islogin(func):
    def func1(request,*args,**kwargs):
        #如果登陆,则执行func函数
        if request.session.has_key('uid'):
            return func(request,*args,**kwargs)
        #如果没登陆，则转到login视图/user/login/
        else:
            return redirect('/user/login/')
    return func1