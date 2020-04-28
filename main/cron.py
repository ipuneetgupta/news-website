from blacklist.models import BlackList
def myjob():
    b = BlackList(ip=request.user)
    b.save()