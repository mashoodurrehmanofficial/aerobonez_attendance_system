# Generated by Django 3.2.6 on 2021-08-20 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0036_attendancereport_normal_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancereport',
            old_name='submit_time',
            new_name='submit_date',
        ),
    ]