from django.db import models
from django.contrib.auth.models import User


# Represents candidate data, including personal
# information and eligibility status for scheduling.
class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    apto_agendamento = models.BooleanField(default=False)


# Defines groups of attendance available for candidates
# during self-registration.
class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=255)


# Stores data provided during self-registration, including attendance
# groups and information about COVID-19.
class Autocadastro(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
    grupos_atendimento = models.ManyToManyField(GrupoAtendimento)
    teve_covid_recentemente = models.BooleanField()
    senha = models.CharField(max_length=255)


# Represents healthcare facilities available for examination scheduling.
class EstabelecimentoSaude(models.Model):
    cnes = models.CharField(max_length=7, unique=True)
    nome = models.CharField(max_length=255)


# Records examination appointments, linking candidates to specific
# healthcare facilities.
class Agendamento(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    estabelecimento_saude = models.ForeignKey(EstabelecimentoSaude, on_delete=models.CASCADE)
    data_hora_agendamento = models.DateTimeField()
    agendamento_expirado = models.BooleanField(default=False)


# Provides a consolidated view of the number of appointments per
# facility for the administrative panel.
class PainelAdministrativo(models.Model):
    estabelecimento_saude = models.ForeignKey(EstabelecimentoSaude, on_delete=models.CASCADE)
    quantidade_agendamentos = models.PositiveIntegerField()


# Supplies data for charts showing the quantity of users eligible
# and ineligible for scheduling.
class GraficoUsuarios(models.Model):
    quantidade_aptos = models.PositiveIntegerField()
    quantidade_inaptos = models.PositiveIntegerField()