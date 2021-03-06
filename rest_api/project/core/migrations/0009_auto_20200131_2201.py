# Generated by Django 2.2.9 on 2020-01-31 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200126_2111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_unit',
            field=models.CharField(choices=[('C', '$'), ('P', '%')], default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('N', 'New'), ('P', 'Popular'), ('D', 'Discount')], default='N', max_length=1, null=True),
        ),
    ]
