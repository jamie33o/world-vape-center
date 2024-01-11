# Generated by Django 3.2.23 on 2024-01-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_remove_multioption_option_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='options',
        ),
        migrations.AddField(
            model_name='product',
            name='options',
            field=models.ManyToManyField(blank=True, to='products.MultiOption'),
        ),
    ]