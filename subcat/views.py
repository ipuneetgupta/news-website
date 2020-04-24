from django.shortcuts import render,get_object_or_404,redirect
from .models import SubCat
from cat.models import Cat
def subcat_list(request):
    
     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    subcat = SubCat.objects.all()
    return render(request,'back/subcat_list.html',{'subcat':subcat})

def subcat_add(request):

     #adminlogin start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #adminlogin end

    cat = Cat.objects.all()
    if request.method == "POST":
        subcatName = request.POST.get("subcatName")
        catId = request.POST.get('cat')
        if subcatName == " ":
            error_msg = "U need to enter subcategory Title !!"
            return render(request,'back/error.html',{'error':error_msg})
        else:
            if len(SubCat.objects.filter(subcatName=subcatName)) != 0:
                error_msg = "This SubCategory Already Exist !!"
                return render(request,'back/error.html',{'error':error_msg})
            catName = Cat.objects.get(pk=catId).catName
            b = SubCat(subcatName=subcatName,catName=catName,catId=catId)
            b.save()
            return redirect('subcat_list')
    return render(request,'back/subcat_add.html',{'cat':cat})