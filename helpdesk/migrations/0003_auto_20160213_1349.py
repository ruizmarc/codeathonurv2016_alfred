# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-13 13:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0002_auto_20160212_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.AlterField(
            model_name='pdi',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='helpdesk.Subject'),
        ),
        migrations.AlterField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='helpdesk.Subject'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'last_update'),
        ),
    ]
