# Generated by Django 3.2.4 on 2021-08-03 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0025_auto_20210804_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='uid',
            field=models.CharField(default='09a98cdf-11f7-46d3-8ad3-67b9b8ae0489', max_length=200),
        ),
    ]
