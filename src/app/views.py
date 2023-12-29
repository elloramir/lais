from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth import models as auth_models

from . import forms

@require_GET
def index(request):
	return redirect('login')


@require_http_methods(['POST', 'GET'])
def login(request):
	if request.method == 'GET':
		form_login = forms.Login()
	else:
		form_login = forms.Login(request.POST)

		if form_login.is_valid():
			user = authenticate(
				username=form_login.cleaned_data['cpf'],
				password=form_login.cleaned_data['senha'])

			# inject user into request
			auth_login(request, user)
			print("LOGGED MF")
		else:
			print(form_login.errors)

	return render(request, 'login.html', {
		'form_login': form_login
	})


@require_http_methods(['POST', 'GET'])
def register(request):
	if request.method == 'GET':
		form_candidato = forms.Candidato()
	else:
		form_candidato = forms.Candidato(request.POST)

		if form_candidato.is_valid():
			candidato = form_candidato.save(commit=False)
			candidato.user = auth_models.User.objects.create_user(
				username=candidato.cpf,
				password=form_candidato.cleaned_data['senha'],
			)
			candidato.save()
			candidato.user.save()

			return redirect('login')
		else:
			print(form_candidato.errors)

	return render(request, 'register.html', {
		'form_candidato': form_candidato
	})
