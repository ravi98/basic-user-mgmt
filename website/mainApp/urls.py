from django.urls import path
from . import views


urlpatterns=[
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.signUp, name='sign-up'),
    path('create-post', views.create_post, name='create-post'),
]