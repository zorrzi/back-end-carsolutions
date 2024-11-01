# Generated by Django 5.1.2 on 2024-11-01 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "carros",
            "0003_remove_car_image_url_car_image_url_1_car_image_url_2_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="discount_percentage",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=3,
                null=True,
                verbose_name="Porcentagem de Desconto",
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="is_discounted",
            field=models.BooleanField(default=False, verbose_name="Desconto Aplicado"),
        ),
    ]
