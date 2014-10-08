from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    stars = models.IntegerField(default='1')
    votes = models.IntegerField(default='1')
    description = models.CharField(max_length=160, unique=False, default='Good product, buy me!')
    imagename = models.CharField(max_length=50, unique=False)

class Cart(models.Model):
	user_id = models.ForeignKey(User)
	item_id = models.ForeignKey(Shop)
	qnty = models.IntegerField(default=1)


class User_Votes(models.Model):
	user_id = models.ForeignKey(User)
	item_id = models.ForeignKey(Shop)
