from django.db import models
from tinymce.models import HTMLField
from customers.models import Customer

# Create your models here.
class AI_Agent(models.Model):
    agent_name = models.CharField(max_length=100)

    def __str__(self):
        return self.agent_name
    
class SalesFunnelStageInstruction(models.Model):
    funnel_stage = models.CharField(max_length=50, choices=(('awareness', 'awareness'), ('interest', 'interest'),('decision', 'decision'), ('purchase', 'purchase'), ('active', 'active'), ('dormant', 'dormant')))
    instructions = HTMLField(max_length=500, help_text="write you sales SOP'S depending on the funnel stage you choose. provide instructions to all the above stages")   
    def __str__(self):
        return self.funnel_stage
    
class TaskPipeline(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    follow_up_date = models.DateField(blank=True, null=True)
    follow_up_time = models.TimeField(blank=True, null=True)
    done = models.BooleanField(default=False)
    def __str__(self):
        return self.customer.phone_number
    
class Escalation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reasons = HTMLField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    done = models.BooleanField(default=False)
    def __str__(self):
        return self.customer.phone_number