from django.urls import path
from . import views

app_name = 'rbrlog'

urlpatterns = [
        path('', views.Index.as_view(), name='index'),
        path('login', views.Login.as_view(), name='login'),
        path('register', views.Register.as_view(), name='register'),
        path('log_out', views.Logout.as_view(), name='log_out'),
        path('search_form', views.SearchUser.as_view(), name= 'search_form'),
        path('search_result', views.SearchUser.as_view(), name= 'search_result'),
]