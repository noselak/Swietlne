# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-06 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20170505_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_total_price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=50),
        ),
    ]
