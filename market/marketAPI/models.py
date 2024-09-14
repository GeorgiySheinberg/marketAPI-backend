from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    phone_number = models.CharField(max_length=255)
    type = models.CharField(max_length=255,default='user')
    shop = models.OneToOneField('Shop', on_delete=models.SET_NULL, null=True, blank=True, related_name='user')

    def __str__(self):
        return self.username


class Shop(models.Model):

    name = models.CharField(max_length=100)
    accepting_status = models.BooleanField(default=False)
    shop_url = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Order(models.Model):

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product = models.ManyToManyField('Products', related_name='products', blank=True)

    def __str__(self):
        return str(self.user)


class OrderProduct(models.Model):

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='order_products')
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order)


class Products(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class ExtraParameter(models.Model):

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='extra_parameters')

    def __str__(self):
        return self.name
