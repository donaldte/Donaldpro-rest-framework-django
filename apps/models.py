from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

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

class ProductQueryset(models.QuerySet):
    def is_public(self):
      return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(name__icontains=query) | Q(description__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs1 = self.filter(user=user).filter((lookup))
            qs  = qs.intersection(qs1)
        return qs   


class  ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQueryset(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user)




      
   

class Product(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=10) 
    public = models.BooleanField(default=True)


    objects = ProductManager()


    @property
    def discount_price(self):
        return "%.2f" %(float(self.price * 0.8))

    def list_something(self):
        return '1234'       


    def __str__(self) -> int:
        return self.name      