from django.shortcuts import render,get_object_or_404,redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
import random
from random import randint
from django.contrib.auth.models import User,Group,Permission
from manager.models import Manager
from news.models import HeadLine
from django.contrib import messages
import string
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from zeep import Client #soup
import requests #curl
from itertools import chain
# Create your views here.

def home(request):
    
    site = Main.objects.get(pk=4)
    # news = News.objects.all().filter(act=1).order_by('-pk')
    latestnews = News.objects.all().filter(act=1).order_by('-pk')[7:13]
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    last3news = News.objects.all().filter(act=1).order_by('-pk')[:3]
    popnews =  News.objects.all().filter(act=1).order_by('-views')[:4]
    pop3news =  News.objects.all().filter(act=1).order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    last4news = News.objects.all().filter(act=1).order_by('-pk')[3:7]

    headline = list()
    for x in cat:
        a = HeadLine.objects.filter(ocatId = x.pk).order_by('-pk')
        headline.append(a[:3])
        if len(headline)>15:
            break
    headline = list(chain(*headline)) 
    
    category_news = list()
    news = list()
    for x in cat:
        a = News.objects.filter(ocatId = x.pk).order_by('-pk')
        category_news.append(a[:2])
        news.append(a[:4])
    news = list(chain(*news))
    category_news = list(chain(*category_news))

    params = {'headline':headline,'category_news':category_news,'site':site,'news':news,'cat':cat,'subcat':subcat,
    'latestnews':latestnews,'last3news':last3news , 
    'popnews':popnews,'pop3news':pop3news,
    'trending':trending,'last4news':last4news}
    
    return render(request,'front/home.html',params)

def about(request):
    site = Main.objects.get(pk=4)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    pop3news =  News.objects.all().order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    news = list()
    for x in cat:
        a = News.objects.filter(ocatId = x.pk).order_by('-pk')
        news.append(a[:4])
    news = list(chain(*news))

    return render(request,'front/about.html',{'site':site,'cat':cat,'subcat':subcat,'news':news,'pop3news':pop3news,'trending':trending})

def panel(request):

    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    
    # #User permission for access for master-user
    # perm = 0
    # perms = Permission.objects.filter(user=request.user)
    # for i in perms:
    #     if i.codename == 'master_user':
    #         perm = 1
    # if perm == 0:
    #     error_msg = "Access Denied !"
    #     return render(request,'back/error.html',{'error':error_msg})
    # #end

    # #Random strong Password Creation
    # ch = ['!','@','#','$','^']
    # randPas = ''
    # for i in range(4):
    #     randPas+=random.choice(string.ascii_letters)
    #     randPas+=random.choice(ch)
    #     randPas+=int(random.randint(0,9))
    # #end creation
    # #random Query
    # count = News.objects.count()
    # randNews = News.objects.all()[random.randint(0,count-1)]
    # #end

    #Humanize Libaray
    #   {% load humanize %}
    #   {{name|function}}
    #

    return render(request,'back/panel.html')

def mylogin(request):
    if request.method == 'POST':
        utxt = request.POST.get('username') 
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt,password=ptxt)
            if user != None:
                login(request,user)
                return redirect('panel')
            else:
                msg = "Wrong Username and Password!!"
                messages.success(request,msg)
                return render(request,'front/mylogin.html')
    return render(request,'front/mylogin.html')

def myregister(request):

    site = Main.objects.get(pk=4)

    if request.method == "POST":
        
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        repassword1 = request.POST.get('repassword1')


        if password1 != repassword1:
            msg = "Password Did'nt Match !"
            messages.success(request,msg)
            return render(request,'front/mylogin.html')

        if len(password1) <= 8 :
            msg = "length of password must be greater than 8 !"
            messages.success(request,msg)
            return render(request,'front/mylogin.html')

        #passwrord Authenicate
        count1=0
        count2=0 
        count3=0 
        # count4=0
        for i in password1:
            if i >= "1" and i <= "9":
                count1=1
            if i >= "a" and i <= "z":
                count2=1
            if i >= "A" and i <= "Z":
                count3=1
            # if i >= "!" and i <= "(":
            #     count4=1
        #complete auth pass

        if count1==0 or count2==0 or count3==0 :
            msg = "Weak Password !"
            messages.success(request,msg)
            return render(request,'front/mylogin.html')

        if len(User.objects.filter(username=username)) == 0 and len(User.objects.filter(email=email))==0:
            #ip,country and city of user extraction 
            ip , isroutable = get_client_ip(request)
            if ip is None:
                ip = '0.0.0.0'
            try:
                response = DbIpCity.get(ip,api_key='free')
                country = response.country + " | " + response.city

            except:
                country = "unknown"
            #end extraction
                
            user = User.objects.create_user(username=username,email=email,password=password1) 
            b = Manager(name=name,e_mail=email,u_name=username,user_ip=ip,country=country)
            msg = "Cograts Account is created !!"
            messages.success(request,msg)
            b.save()
        else:
            msg = "Username or email Already Exist !"
            messages.success(request,msg)
            return render(request,'front/mylogin.html')  
   
    return render(request,'front/mylogin.html')

def mylogout(request):
    logout(request)
    return redirect('home')

def site_setting(request):
    
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

     #permission for access for masteruser
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        error_msg = "Access Denied !"
        return render(request,'back/error.html',{'error':error_msg})
    #end

    if request.method == "POST":
        titleName = request.POST.get('titlename')
        yt = request.POST.get('yt')
        fb = request.POST.get('fb')
        vm = request.POST.get('vm')
        lk = request.POST.get('lk')
        tw = request.POST.get('tw')
        mylink = request.POST.get('mylink')
        about = request.POST.get('about')
        tel = request.POST.get('tel')
        
        if yt == '' : yt = "#"
        if fb == '' : fb = "#"
        if lk == '' : lk = "#"
        if vm == '' : vm = "#"
        if tw == '' : tw = "#"
        if mylink == '' : mylink = "#"

        if titleName==""  or about == "" or tel == "":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})

        try:
            myfile = request.FILES["myfile"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name,myfile)
            url = fs.url(filename)
        except:
            url = '-'
            filename = '-'

        
        try:
            myfile1 = request.FILES["myfile1"]
            fs1 = FileSystemStorage()
            filename1 = fs1.save(myfile1.name,myfile1)
            url1 = fs1.url(filename1)
        except:
            url1 = '-'
            filename1 = '-'


        b = Main.objects.get(pk=4)

        b.titleName = titleName
        b.fb = fb
        b.yt = yt
        b.lk = lk
        b.tw = tw
        b.vm = vm
        b.mylink = mylink
        b.tel = tel
        b.about = about
        if url != '-' and filename != '-':
            if b.imageName != '-':
                fs.delete(b.imageName)
            b.imageUrl = url
            b.imageName = filename

        if url1 != '-' and filename1 != '-':
            if b.imageName1 != '-':
                fs1.delete(b.imageName1)
            b.imageUrl1 = url1
            b.imageName1 = filename1
        b.save()
        
    site = Main.objects.get(pk=4)

    return render(request,'back/setting.html',{'site':site})

def about_setting(request):

     #permission for access for masteruser
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        error_msg = "Access Denied !"
        return render(request,'back/error.html',{'error':error_msg})
    #end
    
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    b = Main.objects.get(pk=4)
    if request.method == 'POST':
        abouttxt = request.POST.get('abouttxt')
        if abouttxt == "":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        b.aboutText = abouttxt
        b.save()
        return redirect('panel')

    return render(request,'back/about_setting.html',{'main':b})

def contact(request):
    
    site = Main.objects.get(pk=4)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.all().order_by('-pk')
    pop3news =  News.objects.all().order_by('-views')[:3]

    return render(request,'front/contact.html',{'site':site,'cat':cat,'subcat':subcat,'news':news,'pop3news':pop3news})

def change_pass(request):
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    
    if request.method == "POST":
        oldpass = request.POST.get('oldpassword')
        newpass = request.POST.get('newpassword')

        if oldpass == "" or newpass == "":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        
        user = authenticate(username=request.user,password=oldpass)

        if user != None:
            if len(newpass) < 8:
                error_msg = "Password Must atleast more than 8 character !"
                return render(request,'back/error.html',{'error':error_msg})

            #passwrord Authenicate
            count1=0
            count2=0 
            count3=0 
            count4=0
            for i in newpass:
                if i >= "1" and i <= "9":
                    count1=1
                if i >= "a" and i <= "z":
                    count2=1
                if i >= "A" and i <= "Z":
                    count3=1
                if i >= "!" and i <= "(":
                    count4=1
            #complete auth pass

            if count1==1 and count2==1 and count3==1 and count4==1:
                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')

        else:
            error_msg = "U need to enter correct old password !"
            return render(request,'back/error.html',{'error':error_msg})

    return render(request,'back/change_pass.html')

def answer_cm(request,pk):
    return render(request,'back/answer_cm.html',{'pk':pk})

def mycovid(request):
    return render(request,'front/corono_table.html')

def privacy(request):
    site = Main.objects.get(pk=4)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    pop3news =  News.objects.all().order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    news = list()
    for x in cat:
        a = News.objects.filter(ocatId = x.pk).order_by('-pk')
        news.append(a[:4])
    news = list(chain(*news))
    d = {'site':site,'cat':cat,'subcat':subcat,'news':news,'pop3news':pop3news,'trending':trending}
    return render(request,'front/privacypolicy.html',d)

def termCondition(request):
    return render(request,'front/term.html')

#soup api
    # client = Client('XXXXXXXwsdl file')
    # result = client.service.funcname(2,3,4) #function need
    # print(result)

    #curl
    # url = ""
    # payload = {'a':"a"}
    # result = requests.post(url,params=payload)
    
    #json
    # url = ""
    # data = {}
    # headers = {'Content_Type':"application/json",'api-key':"XXXX"}
    # result = requests.post(url,data=json.dumps(data),headers=headers)

    #random msg selection start
    # random_object =  Trending.objects.all()[randint(0,len(trending)-1)]
    #end