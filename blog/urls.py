from django.urls import path
from blog import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('new', views.post_new, name='post_new'),
    path('logout', views.logout_view, name='logout'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('following', views.add_follower, name='following'),
    path('request_follower', views.request_follower, name='request_follower'),
    path('request_unfollow', views.request_unfollow, name='request_unfollow'),
]
