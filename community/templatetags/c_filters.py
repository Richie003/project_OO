import re

from django import template
from django.contrib.auth import authenticate, login

from account.forms import UserAdminCreationForm
from account.models import User
from django.shortcuts import redirect, render

register = template.Library()


@register.filter()
def get_midval(value):
    find_val = re.findall("/(.*?)/", value.lstrip('\n'))
    if find_val:
        for i in find_val:
            i = i
        return i
    else:
        return value


@register.inclusion_tag('home/registration.html', takes_context=True)
def registration(context):
    request = context['request']
    form = UserAdminCreationForm
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST or None, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ip = request.META['REMOTE_ADDR']
            instance.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            print('username:', username + 'password:', password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
        return redirect('home')
    contxt = {'form': form}
    return contxt


# @register.filter()
# def summ(value):
#     add = sum(int(value))
#     return int(add)
