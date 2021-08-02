
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('', index, name='index'),     
    path('get_standards', get_standards, name='get_standards'),     
    path('get_classes', get_classes, name='get_classes'),     
    path('get_subjects', get_subjects, name='get_subjects'),     
    path('attendance', attendance, name='attendance'),     
    path('download/<str:filename>', download, name='download'),     
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

