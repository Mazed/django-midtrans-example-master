# Generated by Django 5.1.4 on 2025-01-01 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('midtrans', '0013_alter_order_quantity_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
