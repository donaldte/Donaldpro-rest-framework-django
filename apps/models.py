from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    full_name: str = models.CharField(max_length=50)
    first_name: str = models.CharField(max_length=50)
    last_name: str = models.CharField(max_length=50)
    is_active: bool = models.BooleanField(default=False)
    has_accepted_invite: bool = models.BooleanField(default=False)
    email: str = models.EmailField(null=False, unique=True)
    user: User = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.full_name

class Operation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=False, related_name='received_operations')
    init_date = models.DateTimeField(auto_now_add=True)    

    def __str__(self) -> str:
        return self.person.full_name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=10) 


    @property
    def discount_price(self):
        return "%.2f" %(float(self.price * 0.8))

    def list_something(self):
        return '1234'       


    def __str__(self) -> int:
        return self.name      