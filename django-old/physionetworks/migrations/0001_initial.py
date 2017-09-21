# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-30 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('publishdate', models.DateField(blank=True)),
                ('overview', models.TextField(max_length=1500)),
                ('acknowledgements', models.TextField(blank=True)),
                ('projecttype', models.SmallIntegerField()),
                ('storage', models.SmallIntegerField(default=1)),
                ('requestedstorage', models.SmallIntegerField(default=None)),
                ('associated_pages', models.ManyToManyField(blank=True, related_name='physionetworks_project', to='catalog.Link')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
