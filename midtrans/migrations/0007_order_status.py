# Generated by Django 5.1.4 on 2024-12-31 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('midtrans', '0006_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
