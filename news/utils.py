import random
import datetime
from news.models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
from django.contrib import messages
from comment.models import Comment
from django.core.paginator import Paginator,PageNotAnInteger,Page,EmptyPage
import random
from itertools import chain

def randomNumGen():
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

    #random No Generator
    randhelper = day+month+year+hr+min
    rand =  str(random.randint(1000,9999))
    rand = int(rand + randhelper)

    while(len(News.objects.filter(rand = rand))!=0):
        randhelper = day+month+year+hr+min
        rand =  str(random.randint(1000,9999))
        rand = int(rand + randhelper)
    #end rand generator
    return rand