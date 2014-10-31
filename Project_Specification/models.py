from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Message(models.Model):
    text = models.CharField(max_length=2048)
    sender = models.ForeignKey(WebChatUser)
    receiver = models.ForeignKey(WebChatUser)
    date = models.DateTimeField(default=datetime.now)
    message_picture = models.ImageField(upload_to="webchat_message_photos", blank=True)
    def __unicode__(self):
        return self.text

class WebChatUser(User):
    friends = models.ManyToManyField(WebChatUser)
    email = models.CharField(max_length=256)
    age   = models.CharField(max_length=3)
    motto  = models.CharField(max_length=256)
    fullname = models.CharField(max_length=128)
    id_picture = models.ImageField(upload_to="webchat_id_photos", blank=True)
    def __unicode__(self):
        return self.id

class Group(models.Model):
    group_name = models.CharField(max_length = 256)
    group_users = models.ManyToManyField(WebChatUser)
    def __unicode__(self):
        return group_name