# Generated by Django 5.0.7 on 2024-09-14 12:30

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinformation',
            name='company_description',
            field=tinymce.models.HTMLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='products_summary',
            field=tinymce.models.HTMLField(blank=True, max_length=500, null=True),
        ),
    ]