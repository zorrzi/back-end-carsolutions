# Generated by Django 5.1.2 on 2024-10-20 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
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
                ("year", models.IntegerField(verbose_name="Ano")),
                ("brand", models.CharField(max_length=100, verbose_name="Marca")),
                ("model", models.CharField(max_length=100, verbose_name="Modelo")),
                ("mileage", models.IntegerField(verbose_name="Kilometragem")),
                (
                    "purchase_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Preço de Compra",
                    ),
                ),
                (
                    "rental_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Preço de Aluguel",
                    ),
                ),
                ("image_url", models.URLField(verbose_name="URL da Imagem")),
                (
                    "is_for_sale",
                    models.BooleanField(default=False, verbose_name="À Venda"),
                ),
                (
                    "is_for_rent",
                    models.BooleanField(default=False, verbose_name="Para Aluguel"),
                ),
            ],
        ),
    ]
