# Generated by Django 4.2.16 on 2024-10-03 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone_no',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='shipping_adress',
            new_name='shipping_address',
        ),
    ]
