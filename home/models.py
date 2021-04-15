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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    productId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productId')
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("productId", "user"),)

    def __str__(self):
        return f'{self.user} | {self.productId.__str__()} | {self.quantity}'


class Promotion(models.Model):
    promoDesc = models.CharField(max_length=25)
    promoImage = models.ImageField(upload_to='promo/images/')

    def __str__(self):
        return self.promoDesc


