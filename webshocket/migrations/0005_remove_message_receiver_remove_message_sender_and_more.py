# Generated by Django 5.1.5 on 2025-01-29 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webshocket', '0004_snacks_order_snacksitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
