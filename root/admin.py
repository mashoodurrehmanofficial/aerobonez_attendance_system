from django.contrib import admin
from .models import *
# Register your models here.


from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('root')

for model_name, model in app.models.items():
    admin.site.register(model)