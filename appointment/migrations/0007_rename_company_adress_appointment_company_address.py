# Generated by Django 5.1.5 on 2025-01-23 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0006_additionalvisitor_img_appointment_visitor_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='company_adress',
            new_name='company_address',
        ),
    ]
