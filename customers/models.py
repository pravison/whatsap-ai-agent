from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    whatsapp_profile = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField( blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.whatsapp_profile
    
class Chat(models.Model):
    message = models.HTMLField()
    role = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)

    def __str__(self):
        return self.role