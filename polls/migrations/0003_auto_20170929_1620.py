# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_poll_target_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'участник голосования', 'verbose_name_plural': 'участники голосования'},
        ),
        migrations.AlterModelOptions(
            name='poll',
            options={'verbose_name': 'голосование', 'verbose_name_plural': 'голосования'},
        ),
        migrations.AlterField(
            model_name='participant',
            name='poll',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Poll', verbose_name='Голосование'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='user_information',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.StudentInfo', verbose_name='Инфо о студенте'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='voted',
            field=models.BooleanField(default=False, verbose_name='Проголосовал'),
        ),
    ]