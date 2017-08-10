#coding=utf-8
import datetime
from hashlib import sha1

from django.http import JsonResponse
from django.shortcuts import render,redirect
from ttsx_goods.models import GoodsInfo

import decorator
from models import UserInfo


# Create your views here.
def register(request):
    context = {'title':'注册','top':'0'}
    return render(request,'ttsx_user/register.html',context)

def register_handle(request):
    #提交用户的输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    ucpw = post.get('user_cpwd')
    uemail = post.get('user_email')

    # context={}
    # #如果来源于客户端的验证不准确，最好再验证一次,每个都要重新验证一遍
    # if len(uname)<5 or len(uname)>20:
    #     context['error_name']='请输入5-20个字符的用户名'
    #     context['uname']=uname
    #     return render(request,'ttsx_user/register.html',context)
    # elif

    #对密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    #导入表,将用户注册输入的数据放入数据表中
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')
def register_valid(request):
    #接收用户名
    uname = request.GET.get('uname')
    #查询当前用户的个数
    data = UserInfo.objects.filter(uname=uname).count()
    #返回json{‘valid’:1或0}
    context = {'valid':data}
    return JsonResponse(context)


def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'登录','uname':uname,'top':'0'}
    return render(request,'ttsx_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('user_name')

    upwd = post.get('user_pwd')
    print upwd
    ujz = post.get('user_jz',0)

    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    print upwd_sha1


    context = {'title':'登录','uname':uname,'upwd':upwd,'top':'0'}
    #如果没有查到数据返回【】，如果查到数据返回【UserInfo】
    result = UserInfo.objects.filter(uname=uname)
    if len(result)==0:
        #用户名不存在
        context['error_name']='用户名错误'
        return render(request,'ttsx_user/login.html',context)
    else:
        if result[0].upwd==upwd_sha1:
            #登录成功
            response=redirect(request.session.get('url_path','/'))
            request.session['uid']=result[0].id
            request.session['uname']=result[0].uname
            #记住用户名
            if ujz=='1':
                response.set_cookie('uname',uname,expires=datetime.datetime.now()+datetime.timedelta(days = 14))
            else:
                response.set_cookie('uname','',max_age=-1)
            return response
        else:
            #密码错误
            context['error_pwd']='密码错误'
            return render(request, 'ttsx_user/login.html', context)


def logout(request):
    #清除数据信息整条记录删掉
    request.session.flush()
    return redirect('/user/login/')


def islogin(request):
    result=0
    if request.session.has_key('uid'):
        result=1
    return JsonResponse({'islogin':result})
@decorator.user_islogin
def user_center_info(request):
    #查询当前登陆的用户对象
    user=UserInfo.objects.get(pk=request.session['uid'])
    #查询最近浏览
    ids=request.COOKIES.get('goods_ids','').split(',')[:-1]#[1,2,3]
    glist=[]
    for id in ids:
        glist.append(GoodsInfo.objects.get(id=id))
    context={'user':user,'glist':glist}
    return render(request,'ttsx_user/user_center_info.html',context)



@decorator.user_islogin
def user_center_order(request):
    context={}
    return render(request,'ttsx_user/user_center_order.html',context)


@decorator.user_islogin
def user_center_site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method=='POST':#POST请求
        post=request.POST
        uconsignee=post.get('uconsignee')
        uaddress=post.get('uaddress')
        ucode=post.get('ucode')
        uphone=post.get('uphone')

        user.uconsignee=uconsignee
        user.uaddress=uaddress
        user.ucode=ucode
        user.uphone=uphone
        user.save()

    context={'user':user}
    return render(request,'ttsx_user/user_center_site.html',context)





