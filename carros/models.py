from django.db import models

class Car(models.Model):
    year = models.IntegerField(verbose_name="Ano")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    model = models.CharField(max_length=100, verbose_name="Modelo")
    mileage = models.IntegerField(verbose_name="Kilometragem")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço de Compra")
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço de Aluguel")
    image_url = models.URLField(verbose_name="URL da Imagem")
    is_for_sale = models.BooleanField(default=False, verbose_name="À Venda")
    is_for_rent = models.BooleanField(default=False, verbose_name="Para Aluguel")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

