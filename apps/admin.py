from django.contrib import admin
from . models import Person, Operation, Product

admin.site.register(Person)
admin.site.register(Operation)
admin.site.register(Product)
# Register your models here.
