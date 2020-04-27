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
import string
from ipware import get_client_ip
# Create your views here.

def home(request):
    site = Main.objects.get(pk=4)
    news = News.objects.all().filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    last3news = News.objects.all().filter(act=1).order_by('-pk')[:3]
    popnews =  News.objects.all().filter(act=1).order_by('-views')
    pop3news =  News.objects.all().filter(act=1).order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    #random msg selection start
    # random_object =  Trending.objects.all()[randint(0,len(trending)-1)]
    #end
    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'last3news':last3news , 'popnews':popnews,'pop3news':pop3news,'trending':trending})

def about(request):
    site = Main.objects.get(pk=4)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.all().order_by('-pk')
    pop3news =  News.objects.all().order_by('-views')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    return render(request,'front/about.html',{'site':site,'cat':cat,'subcat':subcat,'news':news,'pop3news':pop3news,'trending':trending})

def panel(request):

    # #adminlogin start
    # if not request.user.is_authenticated:
    #     return redirect('mylogin')
    # #adminlogin end
    
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
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        if len(password1) <= 8 :
            msg = "length of password must be greater than 8 !"
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        #passwrord Authenicate
        count1=0
        count2=0 
        count3=0 
        count4=0
        for i in password1:
            if i >= "1" and i <= "9":
                count1=1
            if i >= "a" and i <= "z":
                count2=1
            if i >= "A" and i <= "Z":
                count3=1
            if i >= "!" and i <= "(":
                count4=1
        #complete auth pass

        if count1==0 or count2==0 or count3==0 or count4==0:
            msg = "Weak Password !"
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        if len(User.objects.filter(username=username)) == 0 and len(User.objects.filter(email=email))==0:
            ip , isroutable = get_client_ip(request)
            if ip is None:
               ip = '0.0.0.0'
            user = User.objects.create_user(username=username,email=email,password=password1) 
            b = Manager(name=name,e_mail=email,u_name=username,user_ip=ip)
            b.save()
        else:
            msg = "Username or email Already Exist !"
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})
        
    return render(request,'front/mylogin.html')

def mylogout(request):
    logout(request)
    return redirect('mylogin')

def site_setting(request):

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

