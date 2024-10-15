from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # extract tenant domain from request
        tenant_domain = request.get_host() #thi sprovides full domain like tenant.mywebsite.com
        # save product domain with domain url passed
        obj.save(domain_url=tenant_domain)

        

admin.site.register(Product, ProductAdmin)

