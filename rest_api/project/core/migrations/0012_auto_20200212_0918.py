# Generated by Django 2.2.10 on 2020-02-12 08:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200209_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('hex', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Hex color format needs to be #xxx or #xxxxxx', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='core.ItemColor'),
        ),
        migrations.AddField(
            model_name='item',
            name='material',
            field=models.ManyToManyField(related_name='items', to='core.Material'),
        ),
    ]