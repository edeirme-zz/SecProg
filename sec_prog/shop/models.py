from django.db import models


class Shop(models.Model):
    product_name = models.CharField(max_length=50, unique=False)
    price = models.FloatField()