from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from . import views


# NOTE: We still using the Django auth system, but with custom views,
# to make our life easier on future features
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('agendamento/', views.profile, name='agendamento'),
]


if settings.DEBUG:
    urlpatterns = [path('admin/', admin.site.urls)] + urlpatterns
