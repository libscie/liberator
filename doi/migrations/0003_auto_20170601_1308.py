# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 13:08
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doi', '0002_auto_20170601_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='oadoi',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='article',
            name='crossref',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='article',
            name='zenodo_deposit',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
