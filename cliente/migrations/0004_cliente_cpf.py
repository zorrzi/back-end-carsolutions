# Generated by Django 5.1.2 on 2024-10-20 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "cliente",
            "0003_cliente_date_joined_cliente_groups_cliente_is_active_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="cpf",
            field=models.CharField(default="", max_length=11, unique=True),
            preserve_default=False,
        ),
    ]
