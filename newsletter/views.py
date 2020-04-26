from django.shortcuts import render,get_object_or_404,redirect
from .models import NewsLetter
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
# Create your views here.

def news_letter(request):
    if request.method == "POST":
        utxt = request.POST.get("emailOrphone")
        if utxt.find('@') != -1 and utxt.find('.') != -1:
            b = NewsLetter(contactUserTxt=utxt,isEmail=1)
            b.save()
        else:
            try:
                int(utxt)
                b = NewsLetter(contactUserTxt=utxt,isEmail=2)
                b.save()

            except:
                return redirect('home')

    return redirect('home')

def news_letter_email(request):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    userEmailList = NewsLetter.objects.all().filter(isEmail=1)
    return render(request,'back/news_email.html',{'userEmailList':userEmailList})


def news_letter_phone(request):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    userPhoneList = NewsLetter.objects.all().filter(isEmail=2)
    return render(request,'back/news_phone.html',{'userPhoneList':userPhoneList})

def news_letter_del(request,pk,num):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    b = NewsLetter.objects.filter(pk=pk)
    b.delete()
    if int(num) == 1:
        return redirect('news_letter_email')

    return redirect('news_letter_phone')