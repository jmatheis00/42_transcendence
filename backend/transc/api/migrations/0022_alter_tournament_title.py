# Generated by Django 4.2.7 on 2024-04-20 09:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_alter_tournament_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='title',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.MinLengthValidator(3, 'Title is too short, must contain at least 3 characters'), django.core.validators.RegexValidator('^[\\w\\-_ ]+$', message='Title should be a combination of alphanumeric characters, spaces and/or dashes')]),
        ),
    ]
