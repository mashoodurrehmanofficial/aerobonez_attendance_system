# Generated by Django 3.2.4 on 2021-08-25 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0045_auto_20210825_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_subject_model',
            name='class_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student_subject_model',
            name='standard_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]