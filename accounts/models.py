from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class CompanyInformation(models.Model):
    company_name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    company_description =HTMLField(max_length=750, blank=True, null=True)
    products_summary= HTMLField(max_length=750, blank=True, null=True)

    def __str__(self):
        return self.company_name
    

class CompanyWebsitePageLink(models.Model):
    page=  models.CharField(max_length=100)
    page_link = models.URLField()

    def __str__(self):
        return self.page
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    role  = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20)
    # escalate_queries_to_this_staff = models.BooleanField(default=False, help_text='set True if you want whatsapp queries to be escalated to the staf')

    def __str__(self):
        return self.name
