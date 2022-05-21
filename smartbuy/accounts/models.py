from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    product_favorites = models.ManyToManyField(Product)

    address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)

    def __str__(self):
        return self.user.username