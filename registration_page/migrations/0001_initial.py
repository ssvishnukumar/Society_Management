# Generated by Django 4.0.3 on 2022-04-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('flat_no', models.IntegerField(unique=True)),
                ('mobile_no', models.IntegerField(unique=True)),
                ('tower_no', models.IntegerField(unique=True)),
                ('password', models.IntegerField(unique=True)),
            ],
        ),
    ]
