from django.urls import path
from blog import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('new', views.post_new, name='post_new'),
    path('logout', views.logout_view, name='logout')
]
