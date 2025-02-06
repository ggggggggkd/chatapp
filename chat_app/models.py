from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    img = models.ImageField(upload_to='images/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_message = models.TextField(blank=True, null=True)
    last_message_time = models.TimeField(blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(default="", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.