# Generated by Django 5.1.2 on 2024-10-26 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cliente", "0002_cliente_favoritos"),
    ]

    operations = [
        migrations.CreateModel(
            name="CartaoCredito",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_cartao", models.CharField(max_length=16)),
                ("nome_titular", models.CharField(max_length=100)),
                ("data_validade", models.DateField()),
                ("codigo_seguranca", models.CharField(max_length=3)),
                ("salvar_para_futuro", models.BooleanField(default=False)),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cartoes",
                        to="cliente.cliente",
                    ),
                ),
            ],
        ),
    ]
