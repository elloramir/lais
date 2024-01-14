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


class Estabelecimento(models.Model):
    cnes = models.CharField(max_length=7, unique=True)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255)
    logadouro = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    telefone = models.CharField(max_length=20)
    # This value must be update back to 5, every hour 
    vagas = models.IntegerField(default=5)

    def drop_vaga(self):
        if self.vagas > 0:
            self.vagas -= 1
            return True

        return False

    def __str__(self):
        return f'{self.cnes} - {self.razao_social}'


class Agendamento(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def already_gone(self):
        return self.data_hora < timezone.now()

    def scheduler(self, candidato, estabelecimento, horas_str):
        if not estabelecimento.drop_vaga():
            return False

        self.candidato = candidato
        self.estabelecimento = estabelecimento
        self.data_hora = timezone.now()
        self.data_hora = self.data_hora.replace(hour=int(horas_str), minute=0, second=0, microsecond=0)

        hour = self.data_hora.hour
        # weekday = self.data_hora.weekday()
        weekday = 5

        # check if weekday is between wednesday and saturnday
        if weekday < 2 or weekday > 5:
            return False

        # we have to check the age of the candidate according to the hour
        age = candidato.idade()
        if hour == 13 and (age < 18 or age > 29): return false
        if hour == 14 and (age < 30 or age > 39): return false
        if hour == 15 and (age < 40 or age > 49): return false
        if hour == 16 and (age < 50 or age > 59): return false
        if hour == 17 and age < 60: return false

        self.save()
        self.estabelecimento.save()
        return True


    def __str__(self):
        return f'{self.candidato} - {self.estabelecimento} - {self.data_hora}'
