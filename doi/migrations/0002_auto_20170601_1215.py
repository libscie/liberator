# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 12:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doi', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([('doi_prefix', 'doi_suffix')]),
        ),
    ]
