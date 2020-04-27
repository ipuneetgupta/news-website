from django.shortcuts import render,get_object_or_404,redirect
from .models import BlackList
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
from manager.models import Manager
from trending.models import Trending
from django.contrib.auth.models import User , Group , Permission
from django.contrib.contenttypes.models import ContentType
from trending.models import Trending
from django.contrib import messages
import datetime
# Create your views here.

def ip_list(request):
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    #permission for access for masteruser of newslist editor delete
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        a = News.objects.get(pk=pk).publisherName
        if str(a) != str(request.user):
            error_msg = "Access Denied !"
            return render(request,'back/error.html',{'error':error_msg})
    #end.

    iplist = BlackList.objects.all().order_by('-pk')
    return render(request,'back/ip_list.html',{'iplist':iplist})

def ip_add(request):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    #permission for access for masteruser of newslist editor delete
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        a = News.objects.get(pk=pk).publisherName
        if str(a) != str(request.user):
            error_msg = "Access Denied !"
            return render(request,'back/error.html',{'error':error_msg})
    #end

    if request.method=="POST":
        ip = request.POST.get('ip')
        b = BlackList(ip=ip)
        b.save()
    return redirect('ip_list')
def ip_del(request,pk):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    #permission for access for masteruser of newslist editor delete
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        a = News.objects.get(pk=pk).publisherName
        if str(a) != str(request.user):
            error_msg = "Access Denied !"
            return render(request,'back/error.html',{'error':error_msg})
    #end

    b = BlackList.objects.get(pk=pk)
    b.delete()
    return redirect('ip_list')