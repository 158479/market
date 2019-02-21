# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-15 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='类名')),
            ],
            options={
                'verbose_name': '类别管理',
                'verbose_name_plural': '类别管理',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='文章标题')),
                ('body', models.TextField(verbose_name='文章正文')),
                ('created_time', models.DateTimeField(verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='文章作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.Category', verbose_name='文章类别')),
            ],
            options={
                'verbose_name': '文章管理',
                'verbose_name_plural': '文章管理',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标签名称')),
            ],
            options={
                'verbose_name': '标签管理',
                'verbose_name_plural': '标签管理',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myblog.Tag', verbose_name='文章标签'),
        ),
    ]
