from django.db import models
from datetime import datetime
# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = {
	('ELCT','Electronic'),
	('OTHERS','Others'),
	('GENERAL','General'),
}

class Sale(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)
	quantity = models.IntegerField(default=1)
	sold_num = models.IntegerField(default=0)
	avg_rating = models.FloatField(default=0)
	seller = models.ForeignKey(User)
	start_time = models.DateTimeField(default=datetime.now)
	end_time = models.DateTimeField()
	price = models.FloatField(default=0)
	item_pic = models.ImageField(upload_to="item_pictures", blank=True)
	shipping_info = models.CharField(max_length=2048)
	category = models.CharField(max_length = 256, choices = CATEGORY_CHOICES)
	def __unicode__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)
	is_sold = models.NullBooleanField()
	sold_price = models.IntegerField()
	list_time = models.DateTimeField(default=datetime.now)
	rating = models.IntegerField(default=0)
	seller = models.ForeignKey(User,related_name='%(class)s_seller')
	buyer = models.ForeignKey(User,related_name='%(class)s_buyer')
	sale = models.ForeignKey(Sale, blank=True)
	item_pic = models.ImageField(upload_to="item_pictures", blank=True)
	def __unicode__(self):
		return self.name

class Profile(models.Model):
	id_picture = models.ImageField(upload_to="cbay_id_photos", blank=True)
	address = models.CharField(max_length=256)
	phone  = models.CharField(max_length=128)
	user = models.OneToOneField(User)
	account_balance = models.FloatField(default = 5000)
	def __unicode__(self):
		return self.id

class Auction(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)
	start_price = models.FloatField(default=0)
	seller = models.ForeignKey(User,related_name='%(class)s_seller')
	start_time = models.DateTimeField(default=datetime.now)
	end_time = models.DateTimeField(default=datetime.now)
	is_ended = models.NullBooleanField(default=False)
	item_pic = models.ImageField(upload_to="item_pictures", blank=True)
	shipping_info = models.CharField(max_length=2048)
	winner = models.ForeignKey(User, null=True,related_name='%(class)s_winner')
	current_max_bid = models.FloatField(null=True)
	is_paid = models.NullBooleanField(default=False)
	def __unicode__(self):
		return self.id

class Bid(models.Model):
	bidder = models.ForeignKey(User)
	auction = models.ForeignKey(Auction)
	bid_price = models.FloatField()
	bid_time = models.DateTimeField(default=datetime.now)
	def __unicode__(self):
		return self.id

class Order(models.Model):
	sale = models.ForeignKey(Sale, null=True)
	auction = models.ForeignKey(Auction, null=True)
	buyer = models.ForeignKey(User)
	time = models.DateTimeField(default=datetime.now)
	shipping_address = models.CharField(max_length=2048)
	quantity = models.IntegerField(default = 1)
	price = models.FloatField(default=0)
	def __unicode__(self):
		return self.id


class Transaction(models.Model):
	order = models.ForeignKey(Order, null=True)
	sale = models.ForeignKey(Sale, null=True)
	auction = models.ForeignKey(Auction, null=True)
	seller = models.ForeignKey(User,related_name='%(class)s_buyer')
	buyer = models.ForeignKey(User,related_name='%(class)s_seller')
	time = models.DateTimeField(default=datetime.now)
	price = models.FloatField(default=0)
	quantity = models.IntegerField(default=1)
	def __unicode__(self):
		return self.id