from django.shortcuts import render, redirect
from .forms import RegistrationForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from requests import Response
from rest_framework import status
from .models import Post, User
from django.contrib.auth.models import Group

import json
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()

        if request.method=='POST':
            ban_id=request.POST.get('ban-id')
            post_id=request.POST.get('post-id')
            if post_id:
                post=Post.objects.get(id=post_id)
                is_mod=request.user.has_perm('mainApp.delete_post')
                if is_mod or (post and post.author==request.user):
                    post.delete()
            elif ban_id:
                user=User.objects.get(id=ban_id)
                if user and request.user.is_staff:
                    group=Group.objects.get(name='default')
                    group.user_set.remove(user)
            
        return render(request, 'mainApp/home.html', {'posts': posts})
    return redirect('/login')

@permission_required("mainApp.add_post", login_url='/login', raise_exception=True)
@login_required(login_url='/login')
def create_post(request):
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect('/home')
    else:
        form=PostForm()
    return render(request, 'mainApp/create_post.html', {'form': form})

def signUp(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='default')
            group.user_set.add(user)
            login(request, user)
            return redirect('/home')
                 
    else:
        form=RegistrationForm()
    return render(request, 'registration/sign_up.html', {"form": form})