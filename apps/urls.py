from django.urls import path
from .views import *

urlpatterns = [
   path('detail/<int:pk>', product_mixim_views),
   path('create-list', product_list_create_view),
   path('update/<int:pk>', product_update_view),
   path('delete/<int:pk>', product_mixim_views),
]
