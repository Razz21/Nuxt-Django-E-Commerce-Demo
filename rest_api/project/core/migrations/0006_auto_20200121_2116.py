# Generated by Django 2.2.9 on 2020-01-21 20:16

from django.db import migrations, models
import django.db.models.deletion
import project.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200121_2059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addressdefaults',
            options={'verbose_name_plural': 'Addresses defaults'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to=project.core.models.get_upload_path)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.Item')),
            ],
            options={
                'verbose_name': 'Item Image',
                'verbose_name_plural': 'Item Images',
            },
        ),
    ]
