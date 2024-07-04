from re import S
from django.shortcuts import render
from shop.models import Sections


def index(request):
    sections = Sections.objects.all()
    context = {
        'section': sections
    }
    return render(request, 'home/home.html', context)
