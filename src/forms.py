from django import forms
from django.utils import timezone

from . import models


class Login(forms.Form):
    cpf = forms.CharField(required=True)
    senha = forms.CharField(required=True)


    def is_valid(self):
        valid = super(Login, self).is_valid()
        if not valid:
            return False

        # find user
        cpf = self.cleaned_data.get('cpf')
        candidato = models.Candidato.objects.filter(cpf=cpf).first()
        if candidato is None:
            self.add_error('senha', 'CPF ou senha incorretos')
            return False

        # validate password
        senha = self.cleaned_data.get('senha')
        if not candidato.user.check_password(senha):
            self.add_error('senha', 'CPF ou senha incorretos')
            return False

        return True

class Candidato(forms.ModelForm):
    senha = forms.CharField(required=True)
    confirmacao_senha = forms.CharField(required=True)


    class Meta:
        model = models.Candidato
        exclude = ['user']


    def is_valid(self):
        valid = super(Candidato, self).is_valid()
        if not valid:
            return False

        # validate "data_nascimento" to disallow future dates and today
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento >= timezone.now().date():
            self.add_error('data_nascimento', 'Data de nascimento inválida')
            return False

        # validate "senha" and "confirmacao_senha"
        senha = self.cleaned_data.get('senha')
        confirmacao_senha = self.cleaned_data.get('confirmacao_senha')
        if senha != confirmacao_senha:
            self.add_error('senha', 'As senhas não coincidem')
            return False

        # TODO: (ellora) real validation of "CPF"
        # validate "CPF"
        cpf = self.cleaned_data.get('cpf')
        if not len(cpf) == 11:
            self.add_error('cpf', 'CPF inválido')
            return False

        # validate "CPF" uniqueness
        if models.Candidato.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', 'CPF já cadastrado')
            return False

        return True


class EstabelecimentoFilter(forms.Form):
    cnes = forms.CharField(required=False)
    razao_social = forms.CharField(required=False)
