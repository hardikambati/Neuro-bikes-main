# Generated by Django 4.1.3 on 2022-11-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED')], max_length=20),
        ),
    ]
