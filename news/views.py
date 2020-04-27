from django.shortcuts import render,get_object_or_404,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
from django.contrib import messages
from comment.models import Comment
from django.core.paginator import Paginator,PageNotAnInteger,Page,EmptyPage
import random
from django_crontab import models
# Create your views here.
def news_detail(request,word):
  
    site = Main.objects.get(pk=4)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    last3news = News.objects.all().order_by('-pk')[:3]
    popnews =  News.objects.all().order_by('-views')
    pop3news =  News.objects.all().order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    #tag
    if len( News.objects.filter(title=word)) != 0:
        shownews = News.objects.get(title=word)
        tags = shownews.tag
        if tags == ' ':
            tags = tags + str(shownews.catName)+","+"News"

        tags = tags.split(',')

    else: return render(request,'front/error.html')
    #endtag

    #viewupdate
    try:

        b = News.objects.get(title=word)
        b.views = b.views + 1
        b.save()

    except :
        pass
    #endviewupdate
       
    shownews = News.objects.filter(title=word)
    code = News.objects.get(title=word)
    
    cms = Comment.objects.filter(newsId=code.pk,status=1).order_by('-pk')[:3]

    iscommentPresent = 0
    if len(cms) !=0 :
        iscommentPresent = 1
    
    return render(request,'front/news_detail.html',{'shownews':shownews,'site':site,'cat':cat,'popnews':popnews,'pop3news':pop3news,'subcat':subcat,'news':news,'tags':tags,'trending':trending,'cms':cms,'iscommentPresent':iscommentPresent})

def news_detail_shorturl(request,randNum):

    site = Main.objects.get(pk=4)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    last3news = News.objects.all().order_by('-pk')[:3]
    popnews =  News.objects.all().order_by('-views')
    pop3news =  News.objects.all().order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    #tag
    if len( News.objects.filter(rand=randNum)) != 0:
        shownews = News.objects.get(rand=randNum)
        tags = shownews.tag
        if tags == '':
            tags = tags + str(shownews.catName)+","+"News"

        tags = tags.split(',')

    else: return render(request,'front/error.html')
    #endtag

    #viewupdate
    try:

        b = News.objects.get(rand=randNum)
        b.views = b.views + 1
        b.save()

    except :
        pass
    #endviewupdate
       
    shownews = News.objects.filter(rand=randNum)

    return render(request,'front/news_detail.html',{'shownews':shownews,'site':site,'cat':cat,'popnews':popnews,'pop3news':pop3news,'subcat':subcat,'news':news,'tags':tags,'trending':trending})

def news_list(request):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    #permission for access for masteruser of newslist editor delete
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    #Paginator
    if perm == 0:
        news = News.objects.filter(publisherName=request.user)
    elif perm == 1:
        newss = News.objects.all()
        paginator = Paginator(newss,2)
        page = request.GET.get('page')
        try:
            news = paginator.page(page)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            news = paginator.page(1)
         
    return render(request,'back/news_list.html',{'news':news})

def add_news(request):

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

    hr = str(now.hour)
    min = str(now.minute)
    currTime = hr+":"+min

    #random No Generator
    randhelper = day+month+year+hr+min
    rand =  str(random.randint(1000,9999))
    rand = int(rand + randhelper)
    
    while(len(News.objects.filter(rand = rand))!=0):
        randhelper = day+month+year+hr+min
        rand =  str(random.randint(1000,9999))
        rand = int(rand + randhelper)
    #end rand generator

    cat = SubCat.objects.all()

    if request.method == 'POST':
        titleNews = request.POST.get("newsTitle")
        publishDate = request.POST.get("publishDate")
        shortTxt = request.POST.get("shortTxt")
        newsContent = request.POST.get("NewsContent")
        writerName = request.POST.get("writerName")
        catId = request.POST.get("newsCat")
        tag = request.POST.get("tag")
        
        if titleNews==""  or shortTxt == "" or newsContent == "" or writerName == "":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        try:
            myfile = request.FILES["myfile"]
            fs = FileSystemStorage()
            if str(myfile.content_type).startswith('image'):
                if myfile.size < 5000000:
                    
                    filename = fs.save(myfile.name,myfile)
                    url = fs.url(filename)
                    catName = SubCat.objects.get(pk=catId).subcatName
                    ocatId = SubCat.objects.get(pk=catId).catId

                    if publishDate=="":
                        publishDate+= currDate+" | "+currTime
                    if tag == "":
                        tag = tag + str(catName)
                    
                    news = News(ocatId=ocatId,title=titleNews,newsSummary=shortTxt,newsContent=newsContent,writerName=writerName,catName=catName,catId=catId,views=0,newsImageUrl=url,publishDate=publishDate,newsImageName=filename,tag=tag,publisherName=request.user,rand=rand)
                    news.save()

                    count = len(News.objects.filter(ocatId=ocatId)) 
                    b = Cat.objects.get(pk=ocatId)
                    b.newsCount=count
                    b.save()            

                else:
                    fs.delete(filename)
                    error_msg = "error ! ur file is Bigger than 5mb"
                    return render(request,'back/error.html',{'error':error_msg})
            
            else:
                fs.delete(filename)
                error_msg = "error ! ur file is not supported"
                return render(request,'back/error.html',{'error':error_msg})
            
        except:
            error_msg = "error ! u need to upload a file in this form"
            return render(request,'back/error.html',{'error':error_msg})

        return redirect('news_list')
    return render(request,'back/add_news.html',{'cat':cat})

def news_delete(request,pk):

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

    try:
        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.newsImageName)

        ocatId = b.ocatId
        count = len(News.objects.filter(ocatId=ocatId)) 
        p = Cat.objects.get(pk=ocatId)
        p.newsCount=count-1
        p.save()  

        b.delete()
        messages.success(request, 'Successfully News Is Delete !')
    except: 
        error_msg = "Something Wrong!!!"
        return render(request,'back/error.html',{'error':error_msg})

    return redirect('news_list')

def news_edit(request,pk):

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
    
    if len(News.objects.filter(pk=pk))==0:
        error_msg = "News Not Found!!!"
        return render(request,'back/error.html',{'error':error_msg})

    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()
     
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

    hr = str(now.hour)
    min = str(now.minute)
    currTime = hr+":"+min

    if request.method == 'POST':
        titleNews = request.POST.get("newsTitle")
        publishDate = request.POST.get("publishDate")
        shortTxt = request.POST.get("shortTxt")
        newsContent = request.POST.get("NewsContent")
        writerName = request.POST.get("writerName")
        catId = request.POST.get("newsCat")
        tag = request.POST.get("tag")

        if titleNews==""  or shortTxt == "" or newsContent == "" or writerName == "":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        try:
            myfile = request.FILES["myfile"]
            fs = FileSystemStorage()
            
            if str(myfile.content_type).startswith('image'):
                if myfile.size < 5000000:

                    catName = SubCat.objects.get(pk=catId).subcatName
                    ocatId = SubCat.objects.get(pk=catId).catId

                    filename = fs.save(myfile.name,myfile)
                    url = fs.url(filename)

                    if publishDate=="":
                        publishDate+= currDate+" | "+currTime
                    
                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.newsImageName)
                    b.delete()
                    
                    b.newsContent=newsContent
                    b.newsImageName=filename
                    b.newsImageUrl=url
                    b.newsSummary=shortTxt
                    b.title=titleNews
                    b.catName=catName
                    b.publishDate=publishDate
                    b.writerName=writerName
                    b.catId = catId
                    b.ocatId = ocatId
                    b.tag = tag

                    b.save()

                    count = len(News.objects.filter(ocatId=ocatId))        
                    b = Cat.objects.get(pk=ocatId)
                    b.newsCount=count
                    b.save()  

                else:
                    fs.delete(filename)
                    error_msg = "error ! ur file is Bigger than 5mb"
                    return render(request,'back/error.html',{'error':error_msg})
            
            else:
                fs.delete(filename)
                error_msg = "error ! ur file is not supported"
                return render(request,'back/error.html',{'error':error_msg})
            
        except:
            catName = SubCat.objects.get(pk=catId).subcatName
            ocatId = SubCat.objects.get(pk=catId).catId

            if publishDate=="":
                publishDate+= currDate+" | "+currTime
            
            b = News.objects.get(pk=pk)
            
            b.newsContent=newsContent
            b.newsSummary=shortTxt
            b.title=titleNews
            b.catName=catName
            b.publishDate=publishDate
            b.writerName=writerName
            b.catId = catId
            b.ocatId = ocatId
            b.tag = tag
            b.act = 0
            b.save()

            count = len(News.objects.filter(ocatId=ocatId)) 
            b = Cat.objects.get(pk=ocatId)
            b.newsCount=count
            b.save()  

        return redirect('news_list')

    return render(request,'back/news_edit.html',{'pk':pk,'news':news,'cat':cat})

def news_publish(request,pk):

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

    b = News.objects.get(pk=pk)
    b.act = 1
    b.save()

    return redirect('news_list')