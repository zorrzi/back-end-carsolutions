# Generated by Django 5.1.2 on 2024-11-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0013_alter_agendamento_carro'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='carro_ano',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='carro_marca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='carro_modelo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='carro_preco',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
