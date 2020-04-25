from django.contrib.auth.models import Group
from django import template

register = template.Library()

@register.filter(name = "has_group")
def has_group(user,gname):
    return user.groups.filter(name=gname).exists()
