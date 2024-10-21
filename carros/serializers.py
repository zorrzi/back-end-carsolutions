from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'year', 'brand', 'model', 'mileage', 'purchase_price', 'rental_price', 'image_url', 'is_for_sale', 'is_for_rent']
