# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('senate', '0013_employee_importance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='Группа доступа'),
        ),
    ]
