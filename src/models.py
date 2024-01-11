from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

NOT_ALLOWED_GROUPS = [
    "População Privada de Liberdade",
    "Pessoas com Deficiência Institucionalizadas",
    "Pessoas ACAMADAS de 80 anos ou mais"
]


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
    teve_covid_recentemente = models.BooleanField(default=False)


    # We are using a method instead of a property because this flag
    # represent a current state of the Candidato
    def apto_agendamento(self):
        older_than_18 = self.idade() >= 18
        not_recently_covid = not self.teve_covid_recentemente
        not_in_not_allowed_group = not self.grupos_atendimento.filter(nome__in=NOT_ALLOWED_GROUPS).exists()

        return older_than_18 and not_recently_covid and not_in_not_allowed_group


    def idade(self):
        stamp_now = timezone.now()
        # transform date to datetime
        stamp_nasc = timezone.make_aware(
            timezone.datetime.combine(self.data_nascimento, timezone.datetime.min.time()))
        # is not precise, but close enough
        return (stamp_now - stamp_nasc).days // 366


    def __str__(self):
        return self.nome_completo
