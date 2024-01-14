from django import forms
from django.utils import timezone
from validate_docbr import CPF

from . import models

cpf_validator = CPF().validate


class Login(forms.Form):
    cpf = forms.CharField(required=True)
    senha = forms.CharField(required=True)


    def is_valid(self):
        valid = super(Login, self).is_valid()
        if not valid:
            return False

        # find user
        cpf = self.cleaned_data.get('cpf')
        user = models.User.objects.filter(username=cpf).first()
        if not user:
            self.add_error('cpf', 'CPF ou senha incorretos')
            return False

        # validate password
        senha = self.cleaned_data.get('senha')
        if not user.check_password(senha):
            self.add_error('cpf', 'CPF ou senha incorretos')
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

        # future dates and today are invalid
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento >= timezone.localtime().date():
            self.add_error('data_nascimento', 'Data de nascimento inválida')
            return False

        # passwords must match
        senha = self.cleaned_data.get('senha')
        confirmacao_senha = self.cleaned_data.get('confirmacao_senha')
        if senha != confirmacao_senha:
            self.add_error('senha', 'As senhas não coincidem')
            return False

        cpf = self.cleaned_data.get('cpf')
        if not cpf_validator(cpf):
            self.add_error('cpf', 'CPF inválido')
            return False
        
        # CPF value most be unique
        if models.Candidato.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', 'CPF já cadastrado')
            return False

        return True


class EstabelecimentoFilter(forms.Form):
    cnes = forms.CharField(required=False)
    razao_social = forms.CharField(required=False)


class Agendamento(forms.ModelForm):
    horario = forms.ChoiceField(required=True, choices=models.Agendamento.CHOISES)

    class Meta:
        model = models.Agendamento
        fields = ['estabelecimento']


    def cleanup_choises(self, candidato):
        age = candidato.idade()
        now = timezone.localtime()
        hour = now.hour

        selected_hour = 0
        if   age >= 18 and age <= 29 and hour <= 13: selected_hour = 0
        elif age >= 30 and age <= 39 and hour <= 14: selected_hour = 1
        elif age >= 40 and age <= 49 and hour <= 15: selected_hour = 2
        elif age >= 50 and age <= 59 and hour <= 16: selected_hour = 3
        elif age >= 60 and hour < 17: selected_hour = 4

        sufix = now.strftime(' - %A de %B de %Y')

        self.fields['horario'].choices = [(
            selected_hour,
            models.Agendamento.CHOISES[selected_hour][1] + sufix
        )]
