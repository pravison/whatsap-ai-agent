# Generated by Django 5.0.7 on 2024-09-16 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_companyinformation_company_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsappNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp_number', models.CharField(max_length=20)),
                ('whatsapp_business_app_url', models.URLField(max_length=100)),
                ('whatsapp_auth_token', models.CharField(editable=False, max_length=500)),
            ],
        ),
    ]