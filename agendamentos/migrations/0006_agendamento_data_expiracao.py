# Generated by Django 5.1.2 on 2024-10-26 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agendamentos", "0005_alter_agendamento_tipo"),
    ]

    operations = [
        migrations.AddField(
            model_name="agendamento",
            name="data_expiracao",
            field=models.DateField(blank=True, null=True),
        ),
    ]
