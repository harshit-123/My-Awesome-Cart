from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="Blog Home"),
    path('blogpost/<int:id>', views.blogpost, name="blogPost"),
]