from django.db import models


class Shop(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    stars = models.IntegerField(default='1')
    votes = models.IntegerField(default='1')
    description = models.CharField(max_length=160, unique=False, default='Good product, buy me!')
    imagename = models.CharField(max_length=50, unique=False)

class Cart(models.Model):
	user_id = models.IntegerField()
	item_id = models.IntegerField()
	qnty = models.IntegerField(default=1)
	total_price = models.FloatField()

class User_Votes(models.Model):
	user_id = models.IntegerField()
	item_id = models.IntegerField()
