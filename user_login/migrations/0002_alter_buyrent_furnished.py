# Generated by Django 4.0.3 on 2022-04-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrent',
            name='furnished',
            field=models.IntegerField(choices=[(0, 'Not Furnished'), (1, 'FURNISHED')], default=0),
        ),
    ]
