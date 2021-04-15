from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.urls import reverse


class Product(models.Model):
    """ This class inherits the class Model for Product table """
    productName = models.CharField(max_length=100)
    productPrice = models.FloatField(default=0)
    productImage = models.ImageField(upload_to='shop/images/')
    productSlug = models.SlugField(max_length=40, default=productName)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        This method overrides the str method to return the product name
        for the Product Table
        :return: Product Name
        """
        return self.productName

    def get_absolute_url(self):
        """
        This method will get the absolute url for the product details page
        :return: Slug
        """
        return reverse('details', kwargs={'productSlug': self.productSlug})


class Cart(models.Model):
    """ This class inherits the class Model for Cart table """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    productId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productId')
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ This class is to set a composite key for the Cart Table """
        unique_together = (("productId", "user"),)

    def __str__(self):
        """
        This method overrides the str method to return the username
        for the Cart Table
        :return:
        """
        return f'{self.user} | {self.productId.__str__()} | {self.quantity}'

