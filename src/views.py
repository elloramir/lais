from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth import models as auth_models, logout as auth_logout

from . import forms
from . import models


@require_GET
def index(request):
	return redirect('login')


# Django already has a view for login, but we want to customize it
# since we can make it more flexible for our needs
@require_http_methods(['POST', 'GET'])
def login(request):
	if request.method == 'GET':
		form_login = forms.Login()
	else:
		form_login = forms.Login(request.POST)

		if form_login.is_valid():
			user = authenticate(
				username=form_login.cleaned_data.get('cpf'),
				password=form_login.cleaned_data.get('senha'))

			# inject user into request
			auth_login(request, user)

			# get next page to redirect
			next_page = request.GET.get('next') or 'profile'

			return redirect(next_page)
		else:
			print(form_login.errors)

	return render(request, 'login.html', {
		'form_login': form_login
	})


# If we are using a custom login view, so we need a custom logout as well
@login_required
@require_GET
def logout(request):
	auth_logout(request)
	return redirect('index')


# Register is our responsability anyway
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
				password=form_candidato.cleaned_data.get('senha'),
			)
			candidato.user.save()
			candidato.save()

			return redirect('login')
		else:
			print(form_candidato.errors)

	return render(request, 'register.html', {
		'form_candidato': form_candidato
	})


@require_GET
@login_required
def profile(request):
	candidato = models.Candidato.objects.get(user=request.user)

	return render(request, 'profile.html', {
		'candidato': candidato
	})


@require_GET
@login_required
def estabelecimentos(request):
	estabelecimentos = models.Estabelecimento.objects.all()
	filter = forms.EstabelecimentoFilter(request.GET)

	if filter.is_valid():
		estabelecimentos = estabelecimentos.filter(
			cnes__icontains=filter.cleaned_data.get('cnes') or '',
			razao_social__icontains=filter.cleaned_data.get('razao_social') or '')

	return render(request, 'estabelecimentos.html', {
		'estabelecimentos': estabelecimentos,
		'filter': filter
	})