# Generated by Django 4.1.3 on 2022-11-12 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_warranty_warranty_upto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warranty',
            name='warranty_upto',
            field=models.DateField(default=datetime.datetime(2023, 2, 20, 10, 51, 24, 40867)),
        ),
    ]