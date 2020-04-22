from django.shortcuts import render,get_object_or_404,redirect
from .models import Cat

def cat_list(request):
    cat = Cat.objects.all()
    return render(request,'back/cat_list.html',{'cat':cat})

def cat_add(request):
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