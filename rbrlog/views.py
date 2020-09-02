from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def index(request):
    return render(request, template_name='rbrlog/loginout.html')



def login_user(request):


    print(request.POST)


    return HttpResponse("Hi every one")
