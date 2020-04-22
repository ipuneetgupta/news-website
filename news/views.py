from django.shortcuts import render,get_object_or_404,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
# Create your views here.
def news_detail(request,word):
    site = Main.objects.get(pk=2)
    news = News.objects.filter(title=word)
    return render(request,'front/news_detail.html',{'news':news,'site':site})

def news_list(request):
    news = News.objects.all()
    return render(request,'back/news_list.html',{'news':news})

def add_news(request):
    
    # print("----------------------------------")
    # #datetime
    # now = datetime.datetime.now()
    # year = str(now.year)
    # month = str(now.month)
    # day = str(now.day)

    # if len(day) == 1:
    #     day = "0"+day
    # if len(month) == 1:
    #     month = "0"+month
    # print(day+"/"+month+"/"+year)

    # hr = str(now.hour)
    # min = str(now.minute)
    # time = hr+":"+min

    # print(time)
    # print("------------------------------------")

    if request.method == 'POST':
        titleNews = request.POST.get("newsTitle")
        publishDate = request.POST.get("publishDate")
        newCategory = request.POST.get("newsCat")
        shortTxt = request.POST.get("shortTxt")
        newsContent = request.POST.get("NewsContent")
        writerName = request.POST.get("writerName")

        if titleNews=="" or publishDate=="" or shortTxt == "" or newsContent == "" or writerName == "" or newCategory=="":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        try:
            myfile = request.FILES["myfile"]

            if str(myfile.content_type).startswith('image'):
                if myfile.size < 5000000:
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name,myfile)
                    url = fs.url(filename)
                    news = News(title=titleNews,newsSummary=shortTxt,newsContent=newsContent,writerName=writerName,catName=newCategory,catId=0,views=0,newsImageUrl=url,publishDate=publishDate,newsImageName=filename)
                    news.save()
                else:
                    error_msg = "error ! ur file is Bigger than 5mb"
                    return render(request,'back/error.html',{'error':error_msg})
            
            else:
                 error_msg = "error ! ur file is not supported"
                 return render(request,'back/error.html',{'error':error_msg})
            
        except:
            error_msg = "error ! u need to upload a file in this form"
            return render(request,'back/error.html',{'error':error_msg})

        return redirect('news_list')
    return render(request,'back/add_news.html')

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