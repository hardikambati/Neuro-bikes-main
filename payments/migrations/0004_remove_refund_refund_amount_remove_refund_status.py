# Generated by Django 4.1.3 on 2022-11-11 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_refund'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refund',
            name='refund_amount',
        ),
        migrations.RemoveField(
            model_name='refund',
            name='status',
        ),
    ]