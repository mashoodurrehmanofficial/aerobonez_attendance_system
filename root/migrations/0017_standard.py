# Generated by Django 3.2.4 on 2021-08-01 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0016_student_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('class_list', models.ManyToManyField(blank=True, null=True, to='root.ClassList')),
                ('subject_list', models.ManyToManyField(blank=True, null=True, to='root.Subject')),
            ],
        ),
    ]