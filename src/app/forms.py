from django import forms
from . import models

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = models.Candidato
        fields = ['nome_completo', 'data_nascimento', 'cpf']

class AutocadastroForm(forms.ModelForm):
    class Meta:
        model = models.Autocadastro
        fields = ['grupos_atendimento', 'teve_covid_recentemente', 'senha']

class EstabelecimentoSaudeForm(forms.ModelForm):
    class Meta:
        model = models.EstabelecimentoSaude
        fields = ['cnes', 'nome']

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = models.Agendamento
        fields = ['estabelecimento_saude', 'data_hora_agendamento']
