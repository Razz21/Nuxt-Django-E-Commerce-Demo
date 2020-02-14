# Generated by Django 2.2.10 on 2020-02-12 08:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200212_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcolor',
            name='hex',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Hex color format needs to be #xxx or #xxxxxx', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')]),
        ),
    ]
