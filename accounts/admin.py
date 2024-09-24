from django.contrib import admin
from .models import CompanyInformation, CompanyWebsitePageLink, Staff, Whatsapp

# Register your models here.
admin.site.register(CompanyInformation)
admin.site.register(CompanyWebsitePageLink)
admin.site.register(Staff)
admin.site.register(Whatsapp)
