# Generated by Django 3.2.4 on 2021-08-02 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0018_classlist_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='uid',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
