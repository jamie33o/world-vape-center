# Generated by Django 3.2.23 on 2024-01-17 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20240117_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='options',
            field=models.ManyToManyField(blank=True, to='products.MultiOption'),
        ),
    ]