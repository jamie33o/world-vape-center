# Generated by Django 3.2.23 on 2024-03-05 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_auto_20240305_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlineitem',
            name='user',
        ),
    ]
