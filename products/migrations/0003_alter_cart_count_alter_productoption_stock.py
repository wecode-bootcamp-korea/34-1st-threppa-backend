# Generated by Django 4.0.5 on 2022-06-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productcolorimage_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='stock',
            field=models.IntegerField(null=True),
        ),
    ]