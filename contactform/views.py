from django.shortcuts import render,get_object_or_404,redirect
from .models import ContactForm
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
from main.models import Main
import datetime

def contact_add(request):
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

    site = Main.objects.get(pk=4)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        msgtxt = request.POST.get('msg')

        if name == "" or email == "" or msgtxt == "":
            msg = "All field required!"
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        b = ContactForm(name= name,email=email,message=msgtxt,date=currDate,time=currTime)
        b.save()
        msg = "Msg Received! "
        return render(request,'front/msgbox.html',{'msg':msg,'site':site})
            
    return redirect('contact')

def contact_show(request):

    #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    cf = ContactForm.objects.all()
    return render(request,'back/contact_form.html',{'cf':cf})

def contact_del(request,pk):
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end
    b = ContactForm.objects.filter(pk=pk)
    b.delete()
    return redirect('contact_show')

