# Generated by Django 5.1.6 on 2025-03-07 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_productvariant_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products"),
        ),
    ]
