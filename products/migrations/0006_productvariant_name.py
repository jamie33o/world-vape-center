# Generated by Django 5.1.6 on 2025-03-07 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "products",
            "0005_productvariant_remove_productvariation_multi_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="name",
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
