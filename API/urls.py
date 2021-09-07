
from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('get_attendance_data', get_attendance_data, name='get_attendance_data'),   
    path('get_teacher_data', get_teacher_data, name='get_teacher_data'),   
    path('get_class_list', get_class_list, name='get_class_list'),   
    path('get_subject_list', get_subject_list, name='get_subject_list'),   


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# http://54.255.3.66:8000/api/get_attendance_data
# http://54.255.3.66:8000/api/get_subject_list
# http://54.255.3.66:8000/api/get_teacher_data
# http://54.255.3.66:8000/api/get_class_list