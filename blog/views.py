from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from blog.forms import PostForm
from blog.models import Post
from django.contrib.auth import logout, login, authenticate

def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})


def signup_view(request):
    if request.method == 'POST':

        form_sign = UserCreationForm(request.POST)

        if form_sign.is_valid():
            form_sign.save()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

            return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})
    else:
        form_sign = UserCreationForm()
    return render(request, template_name='blog/signup.html',
                  context={'form_sign': form_sign})


def login_view(request):
    if request.method == 'POST':
        form_login = AuthenticationForm(data=request.POST)

        if form_login.is_valid():
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
            return render(request, 'blog/post_list.html', context={'posts': posts, 'user': request.user})

    else:
        form_login = AuthenticationForm()
    return render(request, template_name='blog/login.html',
                  context={'form_login': form_login})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})




def logout_view(request):
    logout(request)

    return redirect('login')
