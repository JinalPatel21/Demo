# Generated by Django 5.2 on 2025-04-08 03:41

import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('first_name', models.CharField(blank=True, null=True)),
                ('last_name', models.CharField(blank=True, null=True)),
                ('is_verify', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Joined')),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
