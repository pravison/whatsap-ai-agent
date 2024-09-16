from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Client, Domain

User = get_user_model()

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('client_name', 'business_name', 'on_trial')

    def save_model(self, request, obj, form, change):
        # Modify schema_name before saving the tenant
        if not change:  # Only modify for new tenants
            obj.schema_name = obj.business_name.lower().replace(' ', '-')  # Use business name (name) for schema_name
        
        # Save the tenant with the modified schema_name
        super().save_model(request, obj, form, change)
        
        # Automatically create a domain for the tenant after saving
        if not change:  # If it's a new tenant (not updating an existing one)
            domain = Domain(
                domain=f'{obj.schema_name}.salesflowpro.xyz',  # Generate domain from schema_name
                tenant=obj,                              # Link domain to the tenant
                is_primary=True                         # Set this as the primary domain
            )
            domain.save()

            from django_tenants.utils import tenant_context
            with tenant_context(obj):  # Switch to the tenant schema
                # Create a superuser for the tenant
                User.objects.create_superuser(
                    username=f'admin_{obj.schema_name}',  # Customize admin username
                    password='defaultpassword123',         # Set a default password
                )

