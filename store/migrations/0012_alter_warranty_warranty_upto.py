# Generated by Django 4.1.3 on 2022-11-11 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_warranty_warranty_upto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warranty',
            name='warranty_upto',
            field=models.DateField(default=datetime.datetime(2022, 11, 13, 11, 9, 15, 19994)),
        ),
    ]
