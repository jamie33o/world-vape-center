# Generated by Django 3.2.23 on 2024-01-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_createdat_review_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='multi_choice',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]