from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
	return redirect('login')

def login(request):
	return render(request, 'login.html')

def register(request):
	return render(request, 'register.html')