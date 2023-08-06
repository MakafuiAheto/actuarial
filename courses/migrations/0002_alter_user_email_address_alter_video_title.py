# Generated by Django 4.2.4 on 2023-08-05 17:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_Address',
            field=models.EmailField(blank=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid Email')]),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=254),
        ),
    ]
