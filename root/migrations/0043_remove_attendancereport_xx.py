# Generated by Django 3.2.6 on 2021-08-20 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0042_alter_attendancereport_submit_date_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancereport',
            name='xx',
        ),
    ]
