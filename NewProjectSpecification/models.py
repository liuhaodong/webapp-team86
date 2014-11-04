from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Item(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)
    owner = models.ForeignKey(CBayUser)
    isAuction = models.NullBooleanField()
    listDate = models.DateTimeField(default=datetime.now)
    item_picture = models.ImageField(upload_to="cbay_item_photos", blank=True)
    quantity = model.DecimalField(default = 0)
    rating = models.FloatField(blank=True)
    def __unicode__(self):
        return self.text

class CBayUser(User):
    following = models.ManyToManyField(CBayUser)
    follower = models.ManyToManyField(CBayUser)
    username = models.CharField(max_length=256)
    accountBalance = models.DecimalField(max_digits=10, decimal_places=2)
    id_picture = models.ImageField(upload_to="cbay_id_photos", blank=True)
    rating = models.FloatField()
    def __unicode__(self):
        return self.id

class Bid(model.Model)
    item = models.ForeignKey(Item)
    startPrice = models.DecimalField(max_digits=10, decimal_places=2)
    startTime = models.TimeField()
    endTime = models.TimeField()
    isEnd = models.NullBooleanField()
    ownner = models.ForeignKey(CBayUser)
    winner = models.ForeignKey(CBayUser, blank = True)
    transaction = models.ForeignKey(Transaction, blank = True)
    def __unicode__(self):
        return self.id


class Transaction(model.Model)
    item = model.ForeignKey(Item)
    seller = model.ForeignKey(CBayUser)
    buyer = model.ForeignKey(CBayUser)
    price = model.DecimalField(max_digits=10)
    shippingAddress = model.OneToOneField(Address)
    def __unicode__(self):
        return self.id

class UserBid(model.Model)
    bid = model.ForeignKey(Bid)
    bidder = model.ForeignKey(CBayUser)
    bidPrice = model.DecimalField(max_digits=10)
    def __unicode__(self):
        return self.id


class Address(model.Model)
    country = model.CharField(max_length=128)
    state = model.CharField(max_length = 128)
    city = model.CharField(max_length = 128)
    street1 = model.CharField(max_length = 256)
    street2 = mdoel.CharField(max_length = 256)
    zipCode = mdoel.CharField(max_length = 10)
    def __unicode__(self):
        return self.id


class Comment(models.Model):
    item = models.ForeignKey(Item)
    content = models.CharField(max_length=2048)
    user = models.ForeignKey(CBayUser)
    def __unicode__(self):
        return self.id