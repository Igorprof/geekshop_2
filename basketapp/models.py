from django.db import models

from authapp.models import User
from mainapp.models import Product

from django.utils.functional import cached_property

class BasketQuerySet(models.QuerySet):

    def delete(self):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super().delete()

class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    @cached_property
    def get_basket_cached(self):
        return Basket.objects.filter(user=self.user)
        # return self.user.basket.select_related()

    def __str__(self):
        return f'Корзина пользователя {self.user.username} | Продукт {self.product.name}'

    def general_price(self):
        return self.product.price*self.quantity

    def total_quantity(self):
        # baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_basket_cached
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        # baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_basket_cached
        return sum(basket.general_price() for basket in baskets)

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

