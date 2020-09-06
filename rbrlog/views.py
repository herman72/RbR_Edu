from django.shortcuts import render
from django.http import HttpResponse
from mongoengine import NotUniqueError, DoesNotExist
from rbrlog.mongo_models import User
from django.contrib.auth.hashers import make_password, check_password

from ipware import get_client_ip


def index(request):
    if request.session.get("Login"):
        return render(request, template_name='rbrlog/SesTrue.html',
                      context={"user_name": request.session.get("User_name")})
    else:
        return render(request, template_name='rbrlog/loginout.html')


def login(request):
    # print(request.POST)
    data = request.POST
    try:
        q = User.objects.get(name=data["user_name"])
    except DoesNotExist:
        return HttpResponse("User Does Not Exist")
    # print(q.to_json())
    if check_password(data["psw"], q["hashed_password"]):
        request.session["Login"] = True
        request.session["User_name"] = data["user_name"]
        # print(request.session.get("Login"))
        return HttpResponse("You are Login successfully")
    else:
        return HttpResponse("Wrong PSW")


def register(request):
    try:
        ip, is_routable = get_client_ip(request)

        data = request.POST
        u = User.objects.create(name=data["user_name"], email=data["email"], ip=ip,
                                hashed_password=make_password(data["psw"]))
        print(u.to_json())
        return HttpResponse("You registered successfully")
    except NotUniqueError:
        return HttpResponse("same Username")


def logout(request):
    print(request.session)
    del request.session["Login"]
    del request.session["User_name"]
    return render(request, template_name='rbrlog/loginout.html')


def ban(request):
    ip, is_routable = get_client_ip(request)


