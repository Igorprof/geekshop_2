from django.contrib import admin
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUserProfile

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ShopUserProfile)
