# Generated by Django 3.2.23 on 2024-01-28 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='product_option',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
