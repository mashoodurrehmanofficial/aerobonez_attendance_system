# Generated by Django 3.2.4 on 2021-08-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0031_attendancereport_submit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='email',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='password',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
