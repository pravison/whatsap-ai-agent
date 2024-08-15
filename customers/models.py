from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    whatsapp_profile = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField( blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f" {self. whatsapp_profile} phone number - {self.phone_number}"
    
class Conversation(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, related_name='conversations')
    sender = models.CharField(max_length=50, choices=(('user', 'user'), ('assistant', 'assistant')))
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
    

