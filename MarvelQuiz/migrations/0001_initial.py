# Generated by Django 3.2.9 on 2021-11-21 18:28

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True, verbose_name='User Name')),
                ('ph_num', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Phone Number')),
                ('password', models.CharField(max_length=20, verbose_name='Password')),
            ],
        ),
    ]
