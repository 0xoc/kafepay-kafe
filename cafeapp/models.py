from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from location_field.models.plain import PlainLocationField
import datetime


# role & description ... ?
# agar har kas bekhad ye user dashte bashe, behtar nist phone number i beshe ?
class User(AbstractUser):

    phone = models.CharField(_('phone number'), max_length=11, unique=True, null=True)

    def __str__(self):
        return self.username


class Shop(models.Model):

    name = models.CharField(max_length=20, blank=False, default='???')
    location = PlainLocationField(based_fields=['city'], zoom=7)
    phones = ArrayField(models.IntegerField(blank=False, default="09???"))
    emails = ArrayField(models.EmailField(blank=True))
    open_times = ArrayField(models.TimeField(blank=False))
    menu_prices_on = models.BooleanField(default=False)
    menu_items_on = models.BooleanField(default=False)
    account_number = models.IntegerField(blank=False)
    shaba = models.IntegerField(blank=False)

    users = models.ManyToManyField(User, related_name="user_shops")

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=20, blank=False, default="???", unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=20, blank=False, default="???")
    ingredients = ArrayField(models.CharField(max_length=20, blank=True))
    price = models.IntegerField(blank=True)

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name


class Table(models.Model):

    number = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.number


class Bill(models.Model):

    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=False, null=False)
    pre_bill = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


class Invoice(models.Model):

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, blank=False, null=False)


class Reserve(models.Model):

    count = models.IntegerField(blank=False, default=0)
    date_time = models.DateTimeField(blank=False, default=datetime.datetime.now())

    tables = models.ManyToManyField(Table, related_name="table_reservations")

    def __str__(self):
        return self.id
