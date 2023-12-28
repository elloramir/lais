from django import forms
from django.utils import timezone
from . import models

NOT_ALLOWED_GROUPS = [
    "População Privada de Liberdade",
    "Pessoas com Deficiência Institucionalizadas",
    "Pessoas ACAMADAS de 80 anos ou mais"
]

class CandidatoForm(forms.ModelForm):
	senha = forms.CharField(required=True)
	confirmacao_senha = forms.CharField(required=True)
	teve_covid_recentemente = forms.BooleanField(required=True)

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
		if 18 > (timezone.now() - age).year
			return False

		# TODO(ellora): real validation of "CPF"
		# validate "CPF"
		cpf = self.cleaned_data['cpf']
		if not len(cpf) == 11:
			return False
		
		# validate "senha" and "confirmacao_senha"
		senha = self.cleaned_data['senha']
		confirmacao_senha = self.cleaned_data['confirmacao_senha']
		if senha != confirmacao_senha:
			return False

		# validate "grupos_atendimento"
		grupos_atendimento = self.cleaned_data['grupos_atendimento']
		for grupo in grupos_atendimento:
			if grupo.nome in NOT_ALLOWED_GROUPS:
				return False

		# validate "teve_covid_recentemente"
		teve_covid_recentemente = self.cleaned_data['teve_covid_recentemente']
		if teve_covid_recentemente:
			return False

		return True