# Generated by Django 5.1.4 on 2024-12-31 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('midtrans', '0008_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='status',
            new_name='order_status',
        ),
    ]
