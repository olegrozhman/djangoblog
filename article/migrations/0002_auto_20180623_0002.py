# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-23 00:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat', to='article.Category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='keywords', related_query_name='keywords', to='article.Keywords', verbose_name='Keywords'),
        ),
        migrations.AlterField(
            model_name='keywords',
            name='name',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Tags'),
        ),
    ]
