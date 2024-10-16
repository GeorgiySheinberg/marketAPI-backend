# Generated by Django 5.1.1 on 2024-10-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketAPI', '0002_order_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='product', through='marketAPI.OrderProduct', to='marketAPI.product'),
        ),
    ]
