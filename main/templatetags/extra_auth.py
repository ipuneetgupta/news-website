from django.contrib.auth.models import Group
from django import template

register = template.Library()

@register.filter(name = "has_group")
def has_group(user,gname):
    return user.groups.filter(name=gname).exists()


@register.filter(name = "check1")
def check1(val):
    return val<=5


@register.filter(name = "check2")
def check2(val):
    if val<=10 and val>=6:
        return True
    else:
        return False

@register.filter(name = "check3")
def check3(val):
    if val<=15 and val>=11:
        return True
    else:
        return False


