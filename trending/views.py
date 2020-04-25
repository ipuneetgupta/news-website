from django.shortcuts import render,get_object_or_404,redirect
from .models import Trending
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat

def trending_add(request):
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    if request.method == "POST":
        title = request.POST.get('trendingnews')
        if title == "":
            error_msg = "error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        b = Trending(title=title)
        b.save()
    trendinglist = Trending.objects.all()

    return render(request,'back/trending_add.html',{'trendinglist':trendinglist})

def trending_del(request,pk):
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    b = Trending.objects.filter(pk=pk)
    b.delete()

    return redirect('trending_add')

def trending_edit(request,pk):
    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    title = Trending.objects.get(pk=pk).title
    if request.method == "POST":
        txt = request.POST.get('trendingnews')
        if txt == "":
            error_msg = "Error ! u need to fill all fields of form"
            return render(request,'back/error.html',{'error':error_msg})
        b = Trending.objects.get(pk=pk)
        b.title = txt
        b.save()
        return redirect('trending_add')

    return render(request,'back/trending_edit.html',{'title':title,'pk':pk})