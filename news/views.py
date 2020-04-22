from django.shortcuts import render,get_object_or_404,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
# Create your views here.
def news_detail(request,word):
    site = Main.objects.get(pk=2)
    news = News.objects.filter(title=word)
    return render(request,'front/news_detail.html',{'news':news,'site':site})

def news_list(request):
    news = News.objects.all()
    return render(request,'back/news_list.html',{'news':news})

def add_news(request):
    
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
            filename = fs.save(myfile.name,myfile)
            url = fs.url(filename)
            if str(myfile.content_type).startswith('image'):
                if myfile.size < 5000000:
                    catName = SubCat.objects.get(pk=catId).catName
                    if publishDate=="":
                        publishDate+= currDate+" | "+currTime
                    
                    news = News(title=titleNews,newsSummary=shortTxt,newsContent=newsContent,writerName=writerName,catName=catName,catId=catId,views=0,newsImageUrl=url,publishDate=publishDate,newsImageName=filename)
                    news.save()
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
    try:
        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.newsImageName)
        b.delete()
    except: 
        error_msg = "Something Wrong!!!"
        return render(request,'back/error.html',{'error':error_msg})

    return redirect('news_list')