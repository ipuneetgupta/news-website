from django.shortcuts import render,get_object_or_404,redirect
from .models import Manager
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

def manager_list(request):
    
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

  
    man_list = Manager.objects.all()
    return render(request,'back/manager_list.html',{'managerlist':man_list})

def manager_del(request,pk):

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

    manager = Manager.objects.get(pk=pk)
    b = User.objects.filter(username=manager.u_name)
    b.delete()
    manager.delete()
    
    return redirect('manager_list')

def manager_group(request):

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


    grouplist = Group.objects.all().exclude(name='masteruser')

    return render(request,'back/manager_group.html',{'grouplist':grouplist})

def manager_group_add(request):

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
    
    if request.method == 'POST':
        name = request.POST.get('groupName')
        if name != "":
            if len(Group.objects.filter(name=name)) == 0:
                group = Group(name=name)
                group.save()

    return redirect('manager_group')

def manager_group_del(request,name):

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
    
    b = Group.objects.filter(name=name)
    b.delete()
                
    return redirect('manager_group')

def users_groups(request,pk):

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

    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.u_name)
    userlist=[]
    for x in user.groups.all():
        userlist.append(x.name)
    grouplist = Group.objects.all().exclude(name="masteruser")

    return render(request,'back/users_groups.html',{'userlist':userlist,'grouplist':grouplist,'pk':pk})

def add_users_to_groups(request,pk):

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
        gname = request.POST.get('gname')
        group = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.u_name)
        user.groups.add(group)

    return redirect('users_groups',pk)

def del_users_to_groups(request,name,pk):

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

    group = Group.objects.get(name=name)
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.u_name)
    user.groups.remove(group)

    return redirect('users_groups',pk)

def manager_perms(request):

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


    permslist = Permission.objects.all().exclude(name='masteruser')

    return render(request,'back/manager_perms.html',{'permslist':permslist})

def manager_perms_del(request,name):

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


    b = Permission.objects.filter(name=name)
    b.delete()

    return redirect('manager_perms')

def manager_perms_add(request):

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

    if request.method == 'POST':
        name = request.POST.get('permsName')
        cname = request.POST.get('cName')
        if len(Permission.objects.filter(codename=cname)) == 0:
            content_type = ContentType.objects.get(app_label = 'main',model='main')
            permission = Permission.objects.create(name=name,codename=cname,content_type=content_type)
        else:
            error_msg = "Already Exist !"
            return render(request,'back/error.html',{'error':error_msg})

    return redirect('manager_perms')

def users_perms(request,pk):

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

    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.u_name)

    permslist=[]
    permission = Permission.objects.filter(user=user)

    for x in permission:
        permslist.append(x.name)
    
    allperms = Permission.objects.all()

    return render(request,'back/users_perms.html',{'permslist':permslist,'pk':pk,'allperms':allperms})

def users_perms_del(request,pk,name):

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

    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.u_name)

    permission = Permission.objects.get(name=name)
    user.user_permissions.remove(permission)

    return redirect('users_perms',pk)

def users_perms_add(request,pk):

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
    if request.method == 'POST':
        pname = request.POST.get('pname')
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.u_name)

        permission = Permission.objects.get(name=pname)
        user.user_permissions.add(permission)

    return redirect('users_perms',pk)

def groups_perms(request,name):

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
    group = Group.objects.get(name=name)
    gpermslist = group.permissions.all()
   
    allperms = Permission.objects.all()

    return render(request,'back/groups_perms.html',{'name':name,'gpermslist':gpermslist,'allperms':allperms})

def groups_perms_del(request,gname,pname):

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

    group = Group.objects.get(name=gname)

    perm = Permission.objects.get(name=pname)
    group.permissions.remove(perm)

    return redirect('groups_perms',gname)

def groups_perms_add(request,gname):

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

    if request.method ==  "POST":
        pname =  request.POST.get('pname')
        group = Group.objects.get(name=gname)

        perm = Permission.objects.get(name=pname)
        group.permissions.add(perm)

    return redirect('groups_perms',gname)







