from django.shortcuts import render,get_object_or_404,redirect
from .models import Cat
from news.models import News
from subcat.models import SubCat
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
from manager.models import Manager
from trending.models import Trending
from django.contrib.auth.models import User , Group , Permission
from django.contrib.contenttypes.models import ContentType
from trending.models import Trending
from django.contrib import messages
import csv
from django.http import HttpResponse

def cat_list(request):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    cat = Cat.objects.all()
    return render(request,'back/cat_list.html',{'cat':cat})

def cat_add(request):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    
    if request.method == "POST":
        catName = request.POST.get("catName")
        if catName == " ":
            error_msg = "U need to enter category Title !!"
            return render(request,'back/error.html',{'error':error_msg})
        else:
            if len(Cat.objects.filter(catName=catName)) != 0:
                error_msg = "This Category Already Exist !!"
                return render(request,'back/error.html',{'error':error_msg})
            b = Cat(catName=catName)
            b.save()
            return redirect('cat_list')
    return render(request,'back/cat_add.html')

def cat_del(request,pk):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    b = Cat.objects.filter(pk=pk)
    b.delete()

    return redirect('cat_list')

def export_cat_csv(request):
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachement:filname:'cat.csv'"
    
    writer = csv.writer(response)
    writer.writerow(["Category Name","News Count"])
    for i in Cat.objects.all():
        writer.writerow([i.catName,i.newsCount])
    return response

def import_cat_csv(request):
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    
    if request.method == "POST":
        myfile = request.FILES['csv_file']
        if not myfile.name.endswith('.csv') and myfile.multiple_chunks():      
            messages.success(request, 'Invalid File Format')
            return redirect('cat_list')

        catfile = myfile.read().decode('utf-8')
        cats = catfile.split('\n')

        for cat in cats:
            b = cat.split(',')
            try:
                if len(Cat.objects.filter(catName=b[0]))==0 and b[0]!='Category Name':
                    b = Cat(catName=b[0],newsCount=b[1])
                    b.save()
            except:
                print("")

                
    return redirect('cat_list')