from django.urls import path
from . import views

app_name = 'rbrlog'

urlpatterns = [
        path('', views.index, name='index'),
        path('login', views.login_user, name='login'),
]