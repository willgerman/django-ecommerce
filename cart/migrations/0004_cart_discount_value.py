# Generated by Django 5.1.1 on 2024-12-03 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
