"""import packages"""
import urllib
from django.views import View
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from blog.models import Post, UserBlog
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm, CommentForm, UserCreationForm, PasswordResetForm, ChangePassForm, \
    AuthenticationFormMyself
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

# from django.contrib.auth.forms import AuthenticationForm

"""Class Based view"""


class PostList(View):
    @method_decorator(login_required(login_url='/blog/login/?next=/blog', redirect_field_name=''))
    def get(self, request):
        login_user = UserBlog.objects.get(username=request.user.username)
        posts = Post.objects.filter(Q(author__in=login_user.following.all()) | Q(author=request.user))
        return render(request, template_name='blog/post_list.html', context={'posts': posts, 'user': request.user})


class Register(View):
    signup_form = UserCreationForm

    def get(self, request):
        form_sign = self.signup_form()
        return render(request, template_name='blog/signup.html',
                      context={'form_sign': form_sign})

    def post(self, request):
        form_sign = self.signup_form(request.POST)
        if form_sign.is_valid():
            user = form_sign.save()
            logout(request)
            login(request, user)

            # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

            return redirect(reverse('blog:post_list'))
        else:
            # form_sign = self.signup_form()
            return render(request, template_name='blog/signup.html',
                          context={'form_sign': form_sign})


class Login(View):
    Login_Form = AuthenticationFormMyself

    def get(self, request):
        try:

            blank_form = self.Login_Form(data={'next': request.GET['next']})
            # blank_form = blank_form(initial={'next':  request.GET})
            return render(request, template_name='blog/login.html',
                          context={'form_login': blank_form})
        except:
            blank_form = self.Login_Form()
            return render(request, template_name='blog/login.html',
                          context={'form_login': blank_form})

    def post(self, request):

        filled_form = self.Login_Form(data=request.POST)
        if filled_form.is_valid():
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
            # return redirect(reverse('blog:post_list'))
            return redirect(request.POST.get('next'))
            # return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})

        else:
            filled_form = self.Login_Form()
            return render(request, template_name='blog/login.html',
                          context={'form_login': filled_form})


class NewPost(View):
    form = PostForm

    @method_decorator(login_required(login_url='/blog/login/?next=/blog/new_post', redirect_field_name=''))
    def get(self, request):

        new_form = self.form()
        return render(request, 'blog/post_edit.html', {'form': new_form})

    @method_decorator(login_required(login_url='/blog/login/?next=/blog/new_post', redirect_field_name=''))
    def post(self, request):
        new_form = self.form(request.POST)
        if new_form.is_valid():
            post = new_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_list')
        else:
            new_form = self.form()
        return render(request, 'blog/post_edit.html', {'form': new_form})


class AddComment(View):
    form = CommentForm

    @method_decorator(
        login_required(login_url='/blog/login/?next=/blog/post/<int:pk>/comment/', redirect_field_name=''))
    def get(self, request, pk):
        blank_comment_form = self.form()
        return render(request, 'blog/add_comment_to_post.html', {'form': blank_comment_form})

    @method_decorator(
        login_required(login_url='/blog/login/?next=/blog/post/<int:pk>/comment/', redirect_field_name=''))
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        fill_comment = self.form(request.POST)

        if fill_comment.is_valid():
            comment = fill_comment.save(commit=False)
            comment.post = post
            comment.author_comment = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)

        else:
            blank_comment_form = self.form()
            return render(request, 'blog/add_comment_to_post.html', {'form': blank_comment_form})


class PostDetails(View):
    @method_decorator(login_required(login_url='/blog/login/?next=/blog/post/<int:pk>', redirect_field_name=''))
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', context={'post': post})


class FollowerList(View):
    # @method_decorator(login_required(login_url='/blog/login/?next=/blog/FollowList',))
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % ('/blog/login', request.path))
        else:
            login_user = UserBlog.objects.get(username=request.user.username)
            return render(request, 'blog/FollowList.html',
                          context={'users': UserBlog.objects.all(), 'loginuser': request.user,
                                   'followers': login_user.following.all()})


class RequestFollow(View):
    @method_decorator(login_required(login_url='/blog/login/?next=/blog/request_follow', redirect_field_name=''))
    def post(self, request):
        user = UserBlog.objects.get(username=request.user.username)
        user_want_follow = UserBlog.objects.get(username=request.POST['username'])

        user.following.add(user_want_follow)

        return HttpResponse(status=200)


class RequestUnfollow(View):
    @method_decorator(login_required(login_url='/blog/login/?next=/blog/request_unfollow', redirect_field_name=''))
    def post(self, request):
        user = UserBlog.objects.get(username=request.user.username)
        user_want_follow = UserBlog.objects.get(username=request.POST['username'])
        user.following.remove(user_want_follow)

        return HttpResponse(status=200)


class Logout(View):
    @method_decorator(login_required(login_url='/blog/login/?next=/blog/logout', redirect_field_name=''))
    def get(self, request):
        logout(request)

        return redirect(reverse('blog:login'))


class ForgetPassForm(View):
    form = PasswordResetForm

    @method_decorator(login_required(login_url='/blog/login/?next=/blog/reset_pass', redirect_field_name=''))
    def get(self, request):
        blank_form = self.form()
        return render(request, 'blog/password_reset_form.html', context={'form': blank_form})

    @method_decorator(login_required(login_url='/blog/login/?next=/blog/reset_pass', redirect_field_name=''))
    def post(self, request):
        filled_form = self.form(request.POST)
        if filled_form.is_valid():

            unique_id = get_random_string(length=32)
            user = UserBlog.objects.get(email=request.POST['email'])
            user.forget_password_code_expiration = datetime.now(timezone.utc)
            user.forget_password_code = unique_id
            user.save()

            file = open("link.txt", "w")
            file.write(request.build_absolute_uri(reverse('blog:change_pass')) + '?' + urllib.parse.urlencode(
                {'email': request.POST['email'], 'code': unique_id}))
            file.close()
            return render(request, 'blog/password_reset_done.html', context={'email': request.POST['email']})
        else:

            return render(request, 'blog/password_reset_form.html', context={'form': filled_form})


class ChangePass(View):
    form = ChangePassForm

    @method_decorator(login_required(login_url='/blog/login/?next=/blog/change_pass', redirect_field_name=''))
    def get(self, request):

        try:

            user = UserBlog.objects.get(Q(forget_password_code=(request.GET['code'])) & Q(email=request.GET['email']))
            if (datetime.now(timezone.utc)) - user.forget_password_code_expiration < timedelta(seconds=30):

                blank_form = self.form(request.GET)

                return render(request, 'blog/change_pass.html', context={'form': blank_form})
            else:
                return HttpResponse(status=400, content='Code Validation timeout')

        except:
            return HttpResponse(status=400, content='bad request')

    @method_decorator(login_required(login_url='/blog/login/?next=/blog/change_pass', redirect_field_name=''))
    def post(self, request):
        filled_form = self.form(request.POST)

        if filled_form.is_valid():
            user = UserBlog.objects.get(Q(forget_password_code=request.POST['code']) & Q(email=request.POST['email']))

            user.password = make_password(request.POST['password11'])
            user.save()

            return redirect(reverse('blog:login'))
        else:
            return render(request, 'blog/change_pass.html', context={'form': filled_form})

# def logout_view(request):
#     logout(request)
#
#     return redirect(reverse('blog:login'))


# def request_follower(request):
#     id_one = UserBlog.objects.get(username=request.user.username)
#     id_two = UserBlog.objects.get(username=request.POST['username'])
#
#     id_one.followers.add(id_two)
#
#     return HttpResponse(status=200)
#

# def request_unfollow(request):
#     id_one = UserBlog.objects.get(username=request.user.username)
#     id_two = UserBlog.objects.get(username=request.POST['username'])
#     id_one.followers.remove(id_two)
#
#     return HttpResponse(status=200)


# def add_follower(request):
#     login_user = UserBlog.objects.get(username=request.user.username)
#     return render(request, 'blog/FollowList.html', context={'users': UserBlog.objects.all(), 'loginuser': request.user,
#                                                            'followers': login_user.followers.all()})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', context={'post': post})


# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author_comment = request.user
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#         return render(request, 'blog/add_comment_to_post.html', {'form': form})


# def post_list(request):
#     login_user = UserBlog.objects.get(username=request.user.username)
#
#     posts = Post.objects.filter(Q(author__in=login_user.followers.all()) | Q(author=request.user))
#     return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})


# def signup_view(request):
#     if request.method == 'POST':
#
#         form_sign = UserCreationForm(request.POST)
#
#         if form_sign.is_valid():
#             user = form_sign.save()
#             logout(request)
#             login(request, user)
#             # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#
#             return redirect(reverse('post_list'))
#             # return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})
#     else:
#         form_sign = UserCreationForm()
#     return render(request, template_name='blog/signup.html',
#                   context={'form_sign': form_sign})
#

# def login_view(request):
#     if request.method == 'POST':
#         form_login = AuthenticationForm(data=request.POST)
#
#         if form_login.is_valid():
#             user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#             login(request, user)
#             # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#             return redirect(reverse('blog:post_list'))
#             # return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})
#
#     else:
#         form_login = AuthenticationForm()
#     return render(request, template_name='blog/login.html',
#                   context={'form_login': form_login})
#

# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})
