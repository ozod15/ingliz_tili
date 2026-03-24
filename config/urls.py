"""
URL configuration for English Verbs Learning App project.
The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('verbs.urls')),
]
