from django.contrib import admin
from home.models import Product, Cart, Profile, Address

# PolarLine models
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(Address)
