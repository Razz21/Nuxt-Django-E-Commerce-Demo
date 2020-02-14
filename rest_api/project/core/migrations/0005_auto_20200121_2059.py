# Generated by Django 2.2.9 on 2020-01-21 19:59

from django.db import migrations, models
import project.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_addressdefaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=project.core.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='itemvariant',
            name='attachment',
            field=models.ImageField(blank=True, upload_to=project.core.models.get_upload_variant_path),
        ),
    ]