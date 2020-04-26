from django.shortcuts import render,get_object_or_404,redirect
from .models import Comment
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


def cm_add_news(request,pk):

    shownews = News.objects.get(pk=pk)

    # #datetime
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)

    if len(day) == 1:
        day = "0"+day
    if len(month) == 1:
        month = "0"+month
    currDate = day+"/"+month+"/"+year

    #end

    hr = str(now.hour)
    min = str(now.minute)
    currTime = hr+":"+min
    if request.method=='POST':
        msg = request.POST.get("msg")
        if request.user.is_authenticated:
            manager = Manager.objects.get(u_name=request.user)
            b = Comment(cm=msg,date=currDate,time=currTime,newsId=pk,uname=request.user,email=manager.e_mail)
            b.save()
            messages.success(request, 'Successfully Comment is Posted')
        else:
            msg = request.POST.get("msg")
            name_ = request.POST.get("name")
            email_ = request.POST.get("email")
            b = Comment(cm=msg,date=currDate,time=currTime,newsId=pk,uname=name_,email=email_)
            b.save()
            messages.success(request, 'Successfully Comment is Posted')

    return redirect('news_detail',word=shownews.title)

def comments_list(request):
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

    commentlist = Comment.objects.all()
    newsTitlelist = []
    for x in commentlist:
        newsid = x.newsId
        b = News.objects.get(pk=newsid)
        newsTitlelist.append(b.title)
    zippeddata = zip(commentlist,newsTitlelist)

    return render(request,'back/comments_list.html',{'zipdata':zippeddata})

def comment_del(request,pk):
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

    b = Comment.objects.filter(pk=pk)
    b.delete()
    messages.success(request,'Succesfully ! comment is deleted')

    return redirect('comments_list')

def comment_status(request,pk):
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

    b = Comment.objects.get(pk=pk)
    b.status = 1
    b.save()
    messages.success(request,'Succesfully ! comment is published')

    return redirect('comments_list')