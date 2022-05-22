
from rest_framework.reverse import reverse

from .validators import validate_name, unique_product_name
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='products-detail', lookup_field='pk', read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    my_list = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    # user_related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    url = serializers.HyperlinkedIdentityField(view_name='products-detail', lookup_field='pk')
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(validators=[validate_name, unique_product_name])
    created_by = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Product
        fields=['url', 'edit_url', 'created_by', 'id', 'name', 'description', 'price', 'discount_price', 'my_list', 'email']

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     print(email)
        
    #     return super().update(instance, validated_data)
    

    def get_edit_url(self, obj):
        # return f"/products/v2/{obj.pk}"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('products-detail', kwargs={'pk':obj.pk}, request=request)    
    def get_my_list(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None    
        return obj.list_something()    
