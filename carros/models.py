# models.py

from django.db import models

class Car(models.Model):
    year = models.IntegerField(verbose_name="Ano")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    model = models.CharField(max_length=100, verbose_name="Modelo")
    mileage = models.IntegerField(verbose_name="Kilometragem")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço de Compra")
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço de Aluguel")
    image_url_1 = models.URLField(verbose_name="URL da Imagem Principal")
    image_url_2 = models.URLField(null=True, blank=True, verbose_name="URL da Segunda Imagem")
    image_url_3 = models.URLField(null=True, blank=True, verbose_name="URL da Terceira Imagem")
    is_for_sale = models.BooleanField(default=False, verbose_name="À Venda")
    is_for_rent = models.BooleanField(default=False, verbose_name="Para Aluguel")
    is_reserved = models.BooleanField(default=False, verbose_name="Reservado")
    is_discounted_sale = models.BooleanField(default=False, verbose_name="Desconto Aplicado na Venda")
    is_discounted_rent = models.BooleanField(default=False, verbose_name="Desconto Aplicado no Aluguel")
    discount_percentage_sale = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Porcentagem de Desconto na Venda")
    discount_percentage_rent = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Porcentagem de Desconto no Aluguel")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
