# Generated by Django 5.1.2 on 2024-10-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carros", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="is_reserved",
            field=models.BooleanField(default=False, verbose_name="Reservado"),
        ),
    ]