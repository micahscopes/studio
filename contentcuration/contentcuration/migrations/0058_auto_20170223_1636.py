# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-24 00:36
from __future__ import unicode_literals

import contentcuration.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentcuration', '0057_auto_20170223_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='deleted',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='channel',
            name='public',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='contentnode',
            name='changed',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='contentnode',
            name='original_channel_id',
            field=contentcuration.models.UUIDField(db_index=True, editable=False, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='checksum',
            field=models.CharField(blank=True, db_index=True, max_length=400),
        ),
    ]
