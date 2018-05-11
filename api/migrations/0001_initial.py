# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-10 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, max_length=50, null=True)),
                ('startTime', models.CharField(max_length=50)),
                ('endTime', models.CharField(max_length=50)),
                ('shiftLength', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DPID', models.CharField(default=False, max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('checkin', models.BooleanField(default=False)),
                ('isAssigned', models.BooleanField(default=False)),
                ('shiftLength', models.CharField(blank=True, max_length=20)),
                ('startTime', models.CharField(blank=True, max_length=10)),
                ('endTime', models.CharField(blank=True, max_length=10)),
                ('isNoShow', models.BooleanField(default=True)),
                ('checkout', models.BooleanField(default=False)),
                ('packageScan', models.CharField(blank=True, max_length=3)),
                ('routingTool', models.CharField(blank=True, max_length=3)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Block')),
            ],
            options={
                'ordering': ('block', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.CharField(max_length=50)),
                ('cluster', models.CharField(max_length=50)),
                ('isAssigned', models.BooleanField(default=False)),
                ('tbaCount', models.CharField(blank=True, max_length=50)),
                ('DP', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ('cluster', 'route'),
            },
        ),
        migrations.CreateModel(
            name='Tba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tba', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Driver')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Route')),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Route'),
        ),
    ]