from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# TODO(ellora): populate this table with the XML data
class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome

class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    grupos_atendimento = models.ManyToManyField(GrupoAtendimento, blank=True)

    def __str__(self):
        return self.nome_completo