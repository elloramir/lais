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
    # represent a current state of the "Candidato"
    def apto_agendamento(self):
        older_than_18 = self.idade() >= 18
        not_recently_covid = not self.teve_covid_recentemente
        not_in_not_allowed_group = not self.grupos_atendimento.filter(nome__in=NOT_ALLOWED_GROUPS).exists()

        return older_than_18 and not_recently_covid and not_in_not_allowed_group


    def idade(self):
        stamp_now = timezone.localtime()
        # Transform date to datetime
        stamp_born = timezone.make_aware(
            timezone.datetime.combine(self.data_nascimento, timezone.datetime.min.time()))
        # Is not precise, but close enough
        return (stamp_now - stamp_born).days // 366


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
    last_update = models.DateTimeField(auto_now=True)


    def agendamento_count(self):
        return Agendamento.objects.filter(estabelecimento=self).count()


    # Get "vagas" and update it if necessary
    def get_vagas(self):
        # If the last update was more than 1 hour ago
        if (timezone.localtime() - self.last_update).seconds // 3600 >= 1:
            self.last_update = timezone.localtime()
            self.vagas = 5
            self.save()

        return self.vagas

    def __str__(self):
        return f'{self.cnes} - {self.razao_social}'


class Agendamento(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Exceptions
    class ValidationError(Exception):
        pass

    # This tuple list is super important to sync all possible
    # choises between the "Agendamento" model and the "Agendamento" form
    # TODO(ellora): Move to forms.py and then import here?
    CHOISES = [
        (0, '13:00'),
        (1, '14:00'),
        (2, '15:00'),
        (3, '16:00'),
        (4, '17:00'),
    ]


    def already_gone(self):
        return self.data_hora < timezone.localtime()


    def scheduler(self, candidato, estabelecimento, horario):
        if estabelecimento.get_vagas() == 0:
            raise Agendamento.ValidationError('Estabelecimento sem vagas')

        # discount one vacancy
        estabelecimento.vagas -= 1

        self.candidato = candidato
        self.estabelecimento = estabelecimento
        # "horario" comes from the "Agendamento Form", so it's esentially a string
        self.data_hora = timezone.datetime.strptime(Agendamento.CHOISES[int(horario)][1], '%H:%M')

        # check if weekday is between wednesday and saturnday
        weekday = self.data_hora.weekday()
        if weekday < 2 or weekday > 5:
            raise Agendamento.ValidationError('Agendamento só pode ser feito entre quarta e sábado')

        # we have to check the age of the candidate according to the hour
        hour = self.data_hora.hour
        age = candidato.idade()

        if (
            hour == 13 and (age < 18 or age > 29) or
            hour == 14 and (age < 30 or age > 39) or
            hour == 15 and (age < 40 or age > 49) or
            hour == 16 and (age < 50 or age > 59) or
            hour == 17 and age < 60
        ):
            raise Agendamento.ValidationError('Horário inválido para a idade do candidato')

        # check if the candidate is already scheduled
        if Agendamento.objects.filter(candidato=candidato, data_hora__date=self.data_hora.date()).exists():
            raise Agendamento.ValidationError('Candidato já agendado')

        self.save()
        self.estabelecimento.save()

    def __str__(self):
        return f'{self.candidato} - {self.estabelecimento} - {self.data_hora}'

