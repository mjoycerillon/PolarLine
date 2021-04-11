from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    productName = models.CharField(max_length=100)
    productPrice = models.FloatField(default=0)
    productImage = models.ImageField(upload_to='shop/images/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
