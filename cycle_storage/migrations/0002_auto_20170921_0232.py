# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicycle',
            name='photo',
            field=models.ImageField(upload_to='bicycles/', verbose_name='Фотография'),
        ),
    ]
