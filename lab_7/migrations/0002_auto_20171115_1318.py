# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-15 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_7', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='address',
            field=models.CharField(default=' ', max_length=400),
        ),
        migrations.AddField(
            model_name='friend',
            name='angkatan',
            field=models.CharField(default=' ', max_length=250),
        ),
        migrations.AddField(
            model_name='friend',
            name='birthday',
            field=models.CharField(default=' ', max_length=250),
        ),
        migrations.AddField(
            model_name='friend',
            name='hometown',
            field=models.CharField(default=' ', max_length=250),
        ),
        migrations.AddField(
            model_name='friend',
            name='mail_code',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AddField(
            model_name='friend',
            name='program',
            field=models.CharField(default=' ', max_length=250),
        ),
    ]