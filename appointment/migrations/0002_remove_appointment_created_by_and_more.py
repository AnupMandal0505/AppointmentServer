# Generated by Django 5.1.5 on 2025-01-20 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]
