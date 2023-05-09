from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import *
from . import forms
from .models import *
from .forms import PostForm, ProfileForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView, DeleteView


def main_page(request):
    posts = Post.objects.order_by('-id')
    return render(request, 'main/main_page.html', {'title': 'Главная страница сайта', 'posts': posts})


def someones_page(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=user)
    return render(request, 'main/someone.html', {'posts': posts})


@login_required(login_url='signin')
def user_page(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)
    return render(request, 'main/user_page.html', {'profile': profile, 'posts': posts})


@login_required(login_url='signin')
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(user=request.user)
            post.user = request.user
            post.save()
            return redirect('home')

    else:
        form = PostForm()
        return render(request, 'main/new_post.html', {'form': form})


def create_us(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Такой email уже существует")
                return redirect('create_us')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Это имя уже занято")
                return redirect('create_us')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Пользователь создан!')
                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, "Пароли не совпадают")
            return redirect('create_us')
    else:
        return render(request, 'main/create_us.html')


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Введенные данные не верны")
            return redirect('sign_in')
    else:
        return render(request, 'main/signin.html')


def log_out(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='signin')
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'main/settings.html', {'form': form})


def search(request):
    if request.method == 'POST':
        searched_username = request.POST.get('searched', '')
        user = User.objects.filter(username=searched_username).first()
        if user:
            posts = Post.objects.filter(user=user)
            return render(request, 'main/search.html', {'searched': searched_username, 'posts': posts})
        else:
            return render(request, 'main/search.html', {'searched': searched_username, 'error': 'No results found'})
    else:
        return render(request, 'main/search.html')


@login_required(login_url='signin')
def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
    return redirect('/')



class PostsUpdateView(UpdateView):
    model = Post
    template_name = 'main/new_post.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostsListView(ListView):
    model = Post
    template_name = 'main/otherus.html'
    context_object_name = 'posts'

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(user__username=username)


class PostsDeleteView(DeleteView):
    model = Post
    template_name = 'main/delete.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
