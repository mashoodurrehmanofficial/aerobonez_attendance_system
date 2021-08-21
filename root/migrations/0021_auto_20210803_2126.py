# Generated by Django 3.2.4 on 2021-08-03 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('root', '0020_auto_20210803_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='is_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('uid', models.CharField(blank=True, default='', max_length=200)),
                ('is_allowed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
