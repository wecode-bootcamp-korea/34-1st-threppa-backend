# Generated by Django 4.0.5 on 2022-06-28 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_size_size_sizes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='count',
            new_name='quantity',
        ),
    ]
