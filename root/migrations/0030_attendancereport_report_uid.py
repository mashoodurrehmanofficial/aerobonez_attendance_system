# Generated by Django 3.2.4 on 2021-08-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0029_attendancereport'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancereport',
            name='report_uid',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
