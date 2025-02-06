from django.contrib import admin

# Register your models here.
from .models import CustomUser, Message

admin.site.register(CustomUser)

admin.site.register(Message)