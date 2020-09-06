from django.shortcuts import render
from django.http import HttpResponse
from mongoengine import NotUniqueError, DoesNotExist
from rbrlog.mongo_models import User, DeviceInfo
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta

from ipware import get_client_ip


def index(request):
    if request.session.get("Login"):
        return render(request, template_name='rbrlog/SesTrue.html',
                      context={"user_name": request.session.get("User_name")})
    else:
        return render(request, template_name='rbrlog/loginout.html')


def login(request):
    # print(request.POST)
    ip, is_routable = get_client_ip(request)
    data = request.POST

    try:
        uip = DeviceInfo.objects.get(ip=ip)
    except:
        uip = DeviceInfo.objects.create(ip=ip)

    if uip.numtry > 3:
        print(datetime.now() - uip.login_time > timedelta(minutes=1))
        print(uip)
        if datetime.now() - uip.login_time > timedelta(minutes=1):
            uip.numtry = 0
            uip.save()


        return HttpResponse("1 min banned")
    else:

        try:
            q = User.objects.get(name=data["user_name"])
        except DoesNotExist:
            uip.numtry += 1
            uip.login_time = datetime.now()
            uip.save()
            return HttpResponse("User Does Not Exist")
        # print(q.to_json())
        if check_password(data["psw"], q["hashed_password"]):
            request.session["Login"] = True
            request.session["User_name"] = data["user_name"]
            # print(request.session.get("Login"))
            uip.numtry = 0
            uip.save()
            return HttpResponse("You are Login successfully")
        else:
            uip.numtry += 1
            uip.login_time = datetime.now()
            uip.save()
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
