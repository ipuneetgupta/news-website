from django.shortcuts import render,get_object_or_404,redirect
from .models import Cat

def cat_list(request):
    cat = Cat.objects.all()
    return render(request,'back/cat_list.html',{'cat':cat})