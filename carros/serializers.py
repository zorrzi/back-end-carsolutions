# serializers.py

from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'id', 'year', 'brand', 'model', 'mileage', 'purchase_price',
            'rental_price', 'image_url_1', 'image_url_2', 'image_url_3',
            'is_for_sale', 'is_for_rent', 'is_reserved', 'is_discounted_sale',
            'is_discounted_rent','discount_percentage_sale', 'discount_percentage_rent'
        ]
