# Generated by Django 3.2.4 on 2021-08-03 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0023_remove_teacherprofile_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='uid',
            field=models.CharField(default='181b5eea-433b-401e-a325-87c1ee34297c', max_length=200),
        ),
    ]
