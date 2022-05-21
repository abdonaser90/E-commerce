from django.db import models
from products.models import Product

# Create your models here.
class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE),
    state = models.BooleanField()
    review = models.TextField(default="")
