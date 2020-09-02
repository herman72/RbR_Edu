from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def Login(request):



