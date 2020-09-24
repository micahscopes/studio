# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-06-13 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0006_auto_20191028_2325"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contentnode",
            name="kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("topic", "Topic"),
                    ("video", "Video"),
                    ("audio", "Audio"),
                    ("exercise", "Exercise"),
                    ("document", "Document"),
                    ("html5", "HTML5 App"),
                    ("slideshow", "Slideshow"),
                    ("h5p", "H5P"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="file",
            name="preset",
            field=models.CharField(
                blank=True,
                choices=[
                    ("high_res_video", "High Resolution"),
                    ("low_res_video", "Low Resolution"),
                    ("video_thumbnail", "Thumbnail"),
                    ("video_subtitle", "Subtitle"),
                    ("video_dependency", "Video (dependency)"),
                    ("audio", "Audio"),
                    ("audio_thumbnail", "Thumbnail"),
                    ("document", "Document"),
                    ("epub", "ePub Document"),
                    ("document_thumbnail", "Thumbnail"),
                    ("exercise", "Exercise"),
                    ("exercise_thumbnail", "Thumbnail"),
                    ("exercise_image", "Exercise Image"),
                    ("exercise_graphie", "Exercise Graphie"),
                    ("channel_thumbnail", "Channel Thumbnail"),
                    ("topic_thumbnail", "Thumbnail"),
                    ("html5_zip", "HTML5 Zip"),
                    ("html5_dependency", "HTML5 Dependency (Zip format)"),
                    ("html5_thumbnail", "HTML5 Thumbnail"),
                    ("h5p", "H5P Zip"),
                    ("h5p_thumbnail", "H5P Thumbnail"),
                    ("slideshow_image", "Slideshow Image"),
                    ("slideshow_thumbnail", "Slideshow Thumbnail"),
                    ("slideshow_manifest", "Slideshow Manifest"),
                ],
                max_length=150,
            ),
        ),
    ]
