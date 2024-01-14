from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth import models as auth_models, logout as auth_logout
from json import dumps as json_dumps

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

			# if user is staff, redirect to "estabelecimentos"
			if request.user.is_staff and next_page == 'profile':
				next_page = 'estabelecimentos'

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
	form_agendamento = forms.Agendamento()
	form_agendamento.fix_horario(candidato)

	return render(request, 'profile.html', {
		'candidato': candidato,
		'form_agendamento': form_agendamento
	})


@require_GET
@staff_member_required
def estabelecimentos(request):
	estabelecimentos = models.Estabelecimento.objects.all()
	filter = forms.EstabelecimentoFilter(request.GET)

	if filter.is_valid() and filter.has_changed():
		# we should use icontains because those fields cold be null
		estabelecimentos = estabelecimentos.filter(
			cnes__icontains=filter.cleaned_data.get('cnes') or '',
			razao_social__icontains=filter.cleaned_data.get('razao_social') or '')

	return render(request, 'estabelecimentos.html', {
		'estabelecimentos': estabelecimentos,
		'filter': filter
	})


@require_POST
@login_required
def agendamento(request):
	candidato = models.Candidato.objects.get(user=request.user)

	if not candidato.apto_agendamento():
		return redirect('profile')

	form_agendamento = forms.Agendamento(request.POST)

	form_agendamento.is_valid()
	# if form_agendamento.is_valid():
	estabelecimento = form_agendamento.cleaned_data.get('estabelecimento')
	time = form_agendamento.cleaned_data.get('horario')
	agendamento = models.Agendamento()

	if agendamento.scheduler(candidato, estabelecimento, "13"):
		print('Agendamento realizado com sucesso')
	else:
		print('Agendamento não pode ser realizado')

	return redirect('profile')


@require_GET
@login_required
def agendamentos(request):
	candidato = models.Candidato.objects.get(user=request.user)
	agendamentos = models.Agendamento.objects.filter(candidato=candidato)

	return render(request, 'agendamentos.html', {
		'agendamentos': agendamentos
	})


@require_GET
@staff_member_required
def graficos(request):
	estabelecimentos = models.Estabelecimento.objects.all()
	labels = estabelecimentos.values_list('razao_social', flat=True)
	data = []

	for it in estabelecimentos:
		data.append(it.agendamento_set.count())

	candidatos = models.Candidato.objects.all()
	aptos_and_not = [0, 0]

	for it in candidatos:
		if it.apto_agendamento():
			aptos_and_not[0] += 1
		else:
			aptos_and_not[1] += 1



	# This is not the fastest way to do dump those lists,
	# but it's safe enough and will be only accessed by staff
	# (which is a very small group of users).
	str_labels = json_dumps(list(labels))
	str_data = json_dumps(data)
	str_aptos_and_not = json_dumps(aptos_and_not)

	return render(request, 'graficos.html', {
		'labels': str_labels,
		'data': str_data,
		'aptos_and_not': str_aptos_and_not
	})