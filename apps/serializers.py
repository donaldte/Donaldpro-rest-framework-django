from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    my_list = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields=['id', 'name', 'description', 'price', 'discount_price', 'my_list']

    def get_my_list(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None    
        return obj.list_something()    
