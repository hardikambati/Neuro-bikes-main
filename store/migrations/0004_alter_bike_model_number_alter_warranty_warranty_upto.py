# Generated by Django 4.1.3 on 2022-11-11 07:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_bike_category_alter_warranty_warranty_upto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='model_number',
            field=models.CharField(max_length=555, unique=True),
        ),
        migrations.AlterField(
            model_name='warranty',
            name='warranty_upto',
            field=models.DateField(default=datetime.datetime(2022, 11, 13, 7, 41, 15, 41196)),
        ),
    ]
