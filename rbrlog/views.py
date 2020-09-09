from http import HTTPStatus
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from mongoengine import NotUniqueError, DoesNotExist
from rbrlog.forms import LoginForm, RegisterForm, SearchForm
from rbrlog.mongo_models import User, DeviceInfo
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from ipware import get_client_ip

# def index(request):
#     if request.session.get("Login"):
#
#         return render(request, template_name='rbrlog/SesTrue.html',
#                       context={"user_name": request.session.get("User_name")})
#     else:
#         login_form = LoginForm()
#         register_form = RegisterForm()
#         return render(request, template_name='rbrlog/loginout.html', context={'login_form': login_form,'register_form':register_form})


# def login(request):
#     # print(request.POST)
#     ip, is_routable = get_client_ip(request)
#     data = request.POST
#     login_form = LoginForm(data)
#
#     try:
#         uip = DeviceInfo.objects.get(ip=ip)
#     except:
#         uip = DeviceInfo.objects.create(ip=ip)
#
#
#     if login_form.is_valid():
#         request.session['Login'] = True
#         request.session['User_name'] = login_form.cleaned_data["user_name"]
#
#         uip.numtry = 0
#         uip.save()
#         return HttpResponse("You are Login successfully")
#     else:
#         if uip.numtry > 3:
#
#             if datetime.now() - uip.login_time > timedelta(minutes=1):
#                 uip.numtry = 0
#                 uip.save()
#             else:
#                 return HttpResponse("1 min banned")
#         else:
#             uip.numtry += 1
#             uip.login_time = datetime.now()
#             uip.save()
#             register_form = RegisterForm()
#         return render(request, template_name='rbrlog/loginout.html', context={'login_form': login_form, 'register_form':register_form})
#


# def register(request):
#     data = request.POST
#
#     ip, is_routable = get_client_ip(request)
#
#     register_form = RegisterForm(data)
#     if register_form.is_valid():
#
#         u = User.objects.create(name=register_form.cleaned_data["user_name"], email=register_form.cleaned_data["email"], ip=ip,
#                                 hashed_password=make_password(register_form.cleaned_data["password"]))
#
#         return HttpResponse("You registered successfully", status=200)
#     else:
#         login_form = LoginForm()
#         return render(request, template_name='rbrlog/loginout.html',
#                       context={'login_form': login_form, 'register_form': register_form})
#

# def logout(request):
#     print(request.session)
#     del request.session["Login"]
#     del request.session["User_name"]
#     login_form = LoginForm()
#     register_form = RegisterForm()
#     return render(request, template_name='rbrlog/loginout.html',context={'login_form': login_form, 'register_form':register_form})

class Index(View):

    def get(self, request):
        if request.session.get("Login"):

            return render(request, template_name='rbrlog/SesTrue.html',
                          context={"user_name": request.session.get("User_name")})
        else:
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, template_name='rbrlog/loginout.html',
                          context={'login_form': login_form, 'register_form': register_form})


class Login(View):
    form_class = LoginForm

    def post(self,request):

        ip, is_routable = get_client_ip(request)
        data = request.POST
        login_form = self.form_class(data)

        try:
            uip = DeviceInfo.objects.get(ip=ip)
        except:
            uip = DeviceInfo.objects.create(ip=ip)

        if login_form.is_valid():
            request.session['Login'] = True
            request.session['User_name'] = login_form.cleaned_data["user_name"]

            uip.numtry = 0
            uip.save()
            return HttpResponse("You are Login successfully")
        else:
            if uip.numtry > 3:

                if datetime.now() - uip.login_time > timedelta(minutes=1):
                    uip.numtry = 0
                    uip.save()
                else:
                    return HttpResponse("1 min banned")
            else:
                uip.numtry += 1
                uip.login_time = datetime.now()
                uip.save()
                register_form = RegisterForm()
            return render(request, template_name='rbrlog/loginout.html',
                          context={'login_form': login_form, 'register_form': register_form})


class Register(View):
    form_class = RegisterForm

    def post(self, request):

        data = request.POST

        ip, is_routable = get_client_ip(request)

        register_form = self.form_class(data)
        if register_form.is_valid():

            u = User.objects.create(name=register_form.cleaned_data["user_name"], email=register_form.cleaned_data["email"],
                                    ip=ip,
                                    hashed_password=make_password(register_form.cleaned_data["password"]))

            return HttpResponse("You registered successfully", status=200)
        else:
            login_form = LoginForm()
            return render(request, template_name='rbrlog/loginout.html',
                          context={'login_form': login_form, 'register_form': register_form})


class Logout(View):

    def get(self, request):
        del request.session["Login"]
        del request.session["User_name"]
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, template_name='rbrlog/loginout.html',
                      context={'login_form': login_form, 'register_form': register_form})


class SearchUser(View):
    form_class = SearchForm

    def get(self, request):

        # data = request.POST

        search_form = self.form_class()

        # user = User.objects.filter(name__contains=search_form.cleaned_data['query'])

        return render(request, template_name='rbrlog/SearchForm.html',
                          context={'form_class':search_form})

    def post(self, request):
        data = request.POST

        user = User.objects.filter(name__contains=data['query'])

        return render(request, template_name='rbrlog/Search Result.html',
                      context={'query': data['query']})




