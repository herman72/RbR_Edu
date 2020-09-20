from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.Register.as_view(), name='signup'),
    path('new_post', views.NewPost.as_view(), name='new_post'),
    path('following', views.add_follower, name='following'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('request_follower', views.request_follower, name='request_follower'),
    path('request_unfollow', views.request_unfollow, name='request_unfollow'),
    path('post/<int:pk>/comment/', views.AddComment.as_view(), name='add_comment_to_post'),
]
