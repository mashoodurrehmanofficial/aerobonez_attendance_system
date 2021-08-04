
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('/teacherpanel', teacherpanel, name='teacherpanel'),   
            path('/mark_attendance', mark_attendance, name='mark_attendance'),  
                path('/get_classes', get_classes, name='get_classes'),     
                path('/get_subjects', get_subjects, name='get_subjects'),  
                path('/submit_attendance_sheet', submit_attendance_sheet, name='submit_attendance_sheet'),  

            path('/view_attendance_directory', view_attendance_directory, name='view_attendance_directory'),  

            path('/teacherpanel/load_attendance_sheet/<str:report_uid>', load_attendance_sheet, name='load_attendance_sheet'),  




    path('/adminpanel', adminpanel, name='adminpanel'),          
    path('/waiting_list_teachers_list_update', waiting_list_teachers_list_update, name='waiting_list_teachers_list_update'),          
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

