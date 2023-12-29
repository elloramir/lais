from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns = [path('admin/', admin.site.urls)] + urlpatterns