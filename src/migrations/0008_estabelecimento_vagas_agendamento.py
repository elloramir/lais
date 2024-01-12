# Generated by Django 5.0 on 2024-01-12 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_estabelecimento_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='estabelecimento',
            name='vagas',
            field=models.IntegerField(default=5),
        ),
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidato')),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estabelecimento')),
            ],
        ),
    ]
