from django.shortcuts import get_object_or_404
from requests import delete
from . models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .permissions import CustomPermissions

from rest_framework import generics, mixins, permissions, authentication
from .authentification import TokenAuthentication

from rest_framework.authtoken.models import Token
@api_view(['GET'])
def getting(request):
    instance = ProductSerializer(data=request.data)
    if instance.is_valid(raise_exception=True):
        instance.save()
    return Response(instance.data)



class StaffPermissionMixims():
    permission_classes = [permissions.IsAdminUser, CustomPermissions]

class QursetMixims():
    user_field = 'user'
    def get_queryset(self, *args, **kwargs):
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user
        return super().get_queryset(*args, **kwargs).filter(**lookup_data)
      

class ProductDetailView(StaffPermissionMixims,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
product_detail_view = ProductDetailView.as_view()        

class ProductListCreateView(StaffPermissionMixims,QursetMixims, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
    
    def perform_create(self, serializer):
        email = serializer.validated_data.pop('email')
        print(email)
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description') or None
        user =self.request.user 
        if description is None:
            description = name
        serializer.save(description=description, user=user)

   
      
        
product_list_create_view = ProductListCreateView.as_view()

class ProductUpdadteView(StaffPermissionMixims, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
   

    def perform_update(self, serializer):
        description = serializer.validated_data.get('description') or None
        if description is None:
            description  = 'You have update'
        serializer.save(description=description)
           
product_update_view = ProductUpdadteView.as_view()

class ProductDeleteView(StaffPermissionMixims, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
product_delete_view = ProductDeleteView.as_view()

@api_view(['GET', 'POST'])
def detail_list_create_view(request, pk=None, *args, **kwargs):
    if request.method == "GET":
        if pk is not None:
            queryset = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(queryset, many=False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)    


    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get('name')
            description = serializer.validated_data.get('description') or None
            if description is None:
                description = name
            serializer.save(description=description)
            return Response(serializer.data)


class ProductMixinsView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs) 

    def perform_update(self, serializer):
        description = serializer.validated_data.get('description') or None
        if description is None:
            description  = 'You have update'
        serializer.save(description=description)      

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description') or None
        if description is None:
            description = name
        serializer.save(description=description)    

product_mixim_views = ProductMixinsView.as_view() 


class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user)
        return results    
            
    


