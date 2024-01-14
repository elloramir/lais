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


class Agendamento(forms.ModelForm):
    horario = forms.ChoiceField(required=True)

    class Meta:
        model = models.Agendamento
        fields = ['estabelecimento']

    def fix_horario(self, candidato):
        age = candidato.idade()
        # hour = timezone.now().hour
        hour = 11
        horarios = []
        if age >= 18 and age <= 29 and hour <= 13: horarios.append('13:00')
        if age >= 30 and age <= 39 and hour <= 14: horarios.append('14:00')
        if age >= 40 and age <= 49 and hour <= 15: horarios.append('15:00')
        if age >= 50 and age <= 59 and hour <= 16: horarios.append('16:00')
        if age >= 60: horarios.append('17:00')

        sufix = timezone.now().strftime(' - %A de %B de %Y')
        self.fields['horario'].choices = [(h, h+sufix) for h in horarios]

