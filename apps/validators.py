from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator

def validate_name(value):
        qs = Product.objects.filter(name__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f"{value} product exist already!")
        return value       


unique_product_name = UniqueValidator(queryset=Product.objects.all())        