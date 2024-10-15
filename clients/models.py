from django.db import models
from tinymce.models import HTMLField  
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.

class Client(TenantMixin):
    client_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200, unique=True)
    paid_until = models.DateField(blank=True, null=True)
    on_trial = models.BooleanField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    refferal_code = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    #schema will be automatically created and synced when saved
    auto_create_schema= True
    auto_drop_schema = True


    def __str__(self):
        return str(self.business_name)

class Domain(DomainMixin):
    pass

# class IntrestedClient(models.Model):
#     name = models.CharField(max_length=200)
#     username = models.CharField(max_length=100, unique=True)
#     business_name = models.CharField(max_length=200, unique=True)
#     created_on = models.DateField(auto_now_add=True)
#     email = models.EmailField(blank=True, null=True)
#     phone = models.CharField(max_length=16, blank=True, null=True)
#     refferal_code = models.CharField(max_length=100, blank=True, null=True)
#     location = models.CharField(max_length=200, blank=True, null=True)
#     password = models.CharField(max_length=200, blank=True, null=True)

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = HTMLField()

    def __str__(self):
        return self.question