# Generated by Django 2.2.10 on 2020-07-16 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0044_auto_20200512_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewcount', models.PositiveIntegerField(default=0)),
                ('running_viewcount', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(default=None)),
                ('core_project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='project.CoreProject')),
            ],
        ),
    ]
