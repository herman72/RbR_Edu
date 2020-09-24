from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup', views.Register.as_view(), name='signup'),
    path('new_post', views.NewPost.as_view(), name='new_post'),
    path('FollowList', views.FollowerList.as_view(), name='FollowList'),
    path('post/<int:pk>', views.PostDetails.as_view(), name='post_detail'),
    path('request_follow', views.RequestFollow.as_view(), name='request_follow'),
    path('request_unfollow', views.RequestUnfollow.as_view(), name='request_unfollow'),
    path('post/<int:pk>/comment/', views.AddComment.as_view(), name='add_comment_to_post'),
    path('reset_pass', views.ForgetPassForm.as_view(), name='reset_pass_form'),
    path('change_pass', views.ChangePass.as_view(), name='change_pass'),
]
