from django import forms
from django.utils import timezone

from . import models

NOT_ALLOWED_GROUPS = [
    "População Privada de Liberdade",
    "Pessoas com Deficiência Institucionalizadas",
    "Pessoas ACAMADAS de 80 anos ou mais"
]

class Login(forms.Form):
	cpf = forms.CharField(required=True)
	senha = forms.CharField(required=True)

	def is_valid(self):
		valid = super(Login, self).is_valid()
		if not valid:
			return False

		# find user
		cpf = self.cleaned_data['cpf']
		candidato = models.Candidato.objects.filter(cpf=cpf).first()
		if candidato is None:
			self.add_error('senha', 'CPF ou senha incorretos')
			return False

		# validate password
		senha = self.cleaned_data['senha']
		if not candidato.user.check_password(senha):
			self.add_error('senha', 'CPF ou senha incorretos')
			return False

		return True

class Candidato(forms.ModelForm):
	senha = forms.CharField(required=True)
	confirmacao_senha = forms.CharField(required=True)
	teve_covid_recentemente = forms.BooleanField(initial=False, required=False)

	class Meta:
		model = models.Candidato
		exclude = ['user']

	def is_valid(self):
		valid = super(CandidatoForm, self).is_valid()
		if not valid:
			return False

		# TODO(ellora): are this considering leap years?
		# validate "data de nascimento"
		age = self.cleaned_data['data_nascimento']
		if (timezone.now().year - age.year) < 18:
			self.add_error('data_nascimento', 'Você deve ter mais de 18 anos')
			return False

		# TODO(ellora): real validation of "CPF"
		# validate "CPF"
		cpf = self.cleaned_data['cpf']
		if not len(cpf) == 11:
			self.add_error('cpf', 'CPF inválido')
			return False
		
		# validate "senha" and "confirmacao_senha"
		senha = self.cleaned_data['senha']
		confirmacao_senha = self.cleaned_data['confirmacao_senha']
		if senha != confirmacao_senha:
			self.add_error('senha', 'As senhas não coincidem')
			return False

		# validate "grupos_atendimento"
		grupos_atendimento = self.cleaned_data['grupos_atendimento']
		for grupo in grupos_atendimento:
			if grupo.nome in NOT_ALLOWED_GROUPS:
				self.add_error('grupos_atendimento', 'Você não pode se cadastrar')
				return False

		# validate "teve_covid_recentemente"
		teve_covid_recentemente = self.cleaned_data['teve_covid_recentemente']
		if teve_covid_recentemente:
			self.add_error('teve_covid_recentemente', 'Você não pode se cadastrar')
			return False

		return True