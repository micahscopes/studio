# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-14 21:59
from __future__ import unicode_literals

from django.db import migrations
from django.db import models

import contentcuration.models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("contentcuration", "0121_auto_20200917_1912"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddIndex(
                    model_name="contentnode",
                    index=models.Index(
                        fields=["assessment_id"],
                        name=contentcuration.models.ASSESSMENT_ID_INDEX_NAME,
                    ),
                ),
            ],
            database_operations=[
                # operation to run custom SQL command (check the output of `sqlmigrate`
                # to see the auto-generated SQL, edit as needed)
                migrations.RunSQL(
                    sql='CREATE INDEX CONCURRENTLY "{index_name}" ON "contentcuration_assessmentitem" ("assessment_id");'.format(
                        index_name=contentcuration.models.ASSESSMENT_ID_INDEX_NAME
                    ),
                    reverse_sql='DROP INDEX "{index_name}"'.format(
                        index_name=contentcuration.models.ASSESSMENT_ID_INDEX_NAME
                    ),
                ),
            ],
        ),
    ]
