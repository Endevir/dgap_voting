# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='sex',
            field=models.IntegerField(choices=[(1, 'male'), (2, 'female')], default=1, verbose_name='Пол'),
        ),
    ]