from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .views import StaffPermissionMixims

class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def perform_create(self, serializer):
        email = serializer.validated_data.pop('email')
        print(email)
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description') or None
        if description is None:
            description = name
        serializer.save(description=description)

        

