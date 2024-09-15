from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    whatsapp_profile = models.CharField(max_length=200, blank=True, null=True)
    funnel_stage = models.CharField(max_length=50, default='awareness', choices=(('awareness', 'awareness'), ('interest', 'interest'),('decision', 'decision'), ('purchase', 'purchase'), ('active', 'active'), ('dormant', 'dormant'))) # active for active customer and dormant for dormant customer
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField( blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add = True)
    last_talked = models.DateField(blank=True, null=True)


    def __str__(self):
        return f" {self. whatsapp_profile} phone number - {self.phone_number}"
    
class Conversation(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, related_name='conversations')
    sender = models.CharField(max_length=50, choices=(('customer', 'customer'), ('AI', 'AI')))
    message = models.TextField()
    date_added = models.DateField(auto_now_add = True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
    

