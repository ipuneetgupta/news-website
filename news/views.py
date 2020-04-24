from django.shortcuts import render,get_object_or_404,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
# Create your views here.
def news_detail(request,word):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    cat = Cat.objects.all()
    site = Main.objects.get(pk=4)
    shownews = News.objects.filter(title=word)
    return render(request,'front/news_detail.html',{'shownews':shownews,'site':site,'cat':cat})

def news_list(request):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    news = News.objects.all()
    return render(request,'back/news_list.html',{'news':news})

def add_news(request):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    
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

    cat = SubCat.objects.all()

    if request.method == 'POST':
        titleNews = request.POST.get("newsTitle")
        publishDate = request.POST.get("publishDate")
        shortTxt = request.POST.get("shortTxt")
        newsContent = request.POST.get("NewsContent")
        writerName = request.POST.get("writerName")
        catId = request.POST.get("newsCat")
        
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

                    news = News(ocatId=ocatId,title=titleNews,newsSummary=shortTxt,newsContent=newsContent,writerName=writerName,catName=catName,catId=catId,views=0,newsImageUrl=url,publishDate=publishDate,newsImageName=filename)
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
    except: 
        error_msg = "Something Wrong!!!"
        return render(request,'back/error.html',{'error':error_msg})

    return redirect('news_list')

def news_edit(request,pk):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    
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
            b.save()

            count = len(News.objects.filter(ocatId=ocatId)) 
            b = Cat.objects.get(pk=ocatId)
            b.newsCount=count
            b.save()  

        return redirect('news_list')

    return render(request,'back/news_edit.html',{'pk':pk,'news':news,'cat':cat})