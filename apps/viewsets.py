from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .views import StaffPermissionMixims

class ProductViewsets(StaffPermissionMixims, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

