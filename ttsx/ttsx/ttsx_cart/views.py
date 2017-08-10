#coding=utf-8
from django.shortcuts import render
from models import *
from ttsx_user.models import UserInfo
from django.http import JsonResponse
from django.db.models import Sum
from ttsx_user.decorator import user_islogin
# Create your views here.
def add(request):
    try:
        uid=request.session.get('uid')
        gid=int(request.GET.get('gid'))
        count=int(request.GET.get('count','1'))

        cart=CartInfo.objects.filter(user_id=uid,goods_id=gid)
        if len(cart)==1:#如果用户uid已经购买了商品gid,则将数量+
            cart1=cart[0]
            cart1.count+=1
            cart1.save()
        else:#用户uid没有购买gid的商品则添加
            cart=CartInfo()
            cart.user_id=uid
            cart.goods_id=gid
            cart.count=count
            cart.save()
        return JsonResponse({'isadd':1})
    except:
        return JsonResponse({'isadd':0})

def count(request):
    uid=int(request.session.get('uid'))
    count1=CartInfo.objects.filter(user_id=uid).count()#10
    #count1=CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count__sum')#字典
    return JsonResponse({'count':count1})


def edit(request):
    id=int(request.GET.get('id'))
    count1=int(request.GET.get('count'))
    cart=CartInfo.objects.get(pk=id)
    cart.count=count1
    cart.save()
    return JsonResponse({'ok':1})

def delete(request):
    id=int(request.GET.get('id'))
    cart=CartInfo.objects.get(id=id)
    cart.delete()
    return JsonResponse({'ok':1})
@user_islogin
def cart(request):
    uid=int(request.session.get('uid'))
    cart_list=CartInfo.objects.filter(user_id=uid)
    context={'title':'购物车','cart_list':cart_list}
    return render(request,'ttsx_cart/cart.html',context)

def order(request):
    user=UserInfo.objects.get(pk=request.session.get('uid'))
    cart_list=CartInfo.objects.filter(id__in=request.POST.getlist('cart_id'))
    context={'title':'提交订单','user':user,'cart_list':cart_list}
    return render(request,'ttsx_cart/place_order.html',context)