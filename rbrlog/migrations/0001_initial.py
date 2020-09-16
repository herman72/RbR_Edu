# Generated by Django 2.2.3 on 2020-09-16 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=255, verbose_name='IP')),
                ('numtry', models.IntegerField(default=0)),
                ('login_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='Login_Time')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('ip', models.CharField(max_length=255, verbose_name='IP')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now)),
                ('hashed_password', models.CharField(max_length=255, verbose_name='PWD')),
            ],
        ),
    ]