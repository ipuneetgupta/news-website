from django.shortcuts import render,get_object_or_404,redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
    site = Main.objects.get(pk=4)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    last3news = News.objects.all().order_by('-pk')[:3]

    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'last3news':last3news})

def about(request):
    site = Main.objects.get(pk=4)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.all().order_by('-pk')
    return render(request,'front/about.html',{'site':site,'cat':cat,'subcat':subcat,'news':news})

def panel(request):
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
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

def mylogout(request):
    logout(request)
    return redirect('mylogin')

def site_setting(request):
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
