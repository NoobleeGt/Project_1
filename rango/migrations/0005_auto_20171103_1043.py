# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-03 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20171102_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.URLField(max_length=128),
        ),
    ]
