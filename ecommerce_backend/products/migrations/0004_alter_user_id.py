# Generated by Django 4.2.16 on 2024-09-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]