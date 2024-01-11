# Generated by Django 3.2.23 on 2024-01-10 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_remove_product_num_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=30)),
                ('options', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='MultiChoice',
        ),
        migrations.RemoveField(
            model_name='product',
            name='choices',
        ),
        migrations.AddField(
            model_name='product',
            name='options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.multioption'),
        ),
    ]