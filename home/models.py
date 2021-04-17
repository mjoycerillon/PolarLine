from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    """ This class inherits the class Model for Profile table """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        This method overrides the str method to return the username
        :return: Username
        """
        return self.user.__str__()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Address(models.Model):
    """ This class inherits the class Model for Address table """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)

    def __str__(self):
        """
        This method overrides the str method to return the username
        :return: Username
        """
        return self.user.__str__()

    @receiver(post_save, sender=User)
    def create_user_address(sender, instance, created, **kwargs):
        if created:
            Address.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_address(sender, instance, **kwargs):
        instance.address.save()


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
        return reverse('details', kwargs={'slug': self.productSlug})


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
