from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request, 'login.html')

def login(request):
	return render(request, 'login.html')

def register(request):
	return render(request, 'register.html')