
from django.urls import path
from .views import *
from .views_admin_panel_db_operations import *
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



    path('/views_admin_panel_db_operations/manage_teachers', manage_teachers, name='manage_teachers'),   
    path('/views_admin_panel_db_operations/manage_teachers_add', manage_teachers_add, name='manage_teachers_add'),   
    # path('/views_admin_panel_db_operations/manage_teachers_update_teacher_record', manage_teachers_update_teacher_record, name='manage_teachers_update_teacher_record'),   
    path('/views_admin_panel_db_operations/manage_teachers_delete/<str:id>', manage_teachers_delete, name='manage_teachers_delete'),   
    path('/views_admin_panel_db_operations/manage_teachers_extract_data/<str:id>', manage_teachers_extract_data, name='manage_teachers_extract_data'),   


    path('/views_admin_panel_db_operations/manage_teachers/allow_teachers', manage_teachers_allow_teachers, name='manage_teachers_allow_teachers'),   
    path('/views_admin_panel_db_operations/manage_teachers/allow_teachers_post/', manage_teachers_allow_teachers_post, name='manage_teachers_allow_teachers_post'),   
    
    
    
    
    
    path('/views_admin_panel_db_operations/manage_standards/', manage_standards, name='manage_standards'),   
    path('/views_admin_panel_db_operations/manage_standards_add/', manage_standards_add, name='manage_standards_add'),   
    path('/views_admin_panel_db_operations/manage_standards_delete/<str:id>', manage_standards_delete, name='manage_standards_delete'),   



    path('/views_admin_panel_db_operations/manage_classes/', manage_classes, name='manage_classes'),   
    path('/views_admin_panel_db_operations/manage_classes_add/', manage_classes_add, name='manage_classes_add'),   
    path('/views_admin_panel_db_operations/manage_classes_delete/', manage_classes_delete, name='manage_classes_delete'),   
    path('/views_admin_panel_db_operations/manage_classes/get_class_students', get_class_students, name='get_class_students'),   




    path('/views_admin_panel_db_operations/manage_students/', manage_students, name='manage_students'),   
    path('/views_admin_panel_db_operations/manage_students_add/', manage_students_add, name='manage_students_add'),   
    path('/views_admin_panel_db_operations/manage_students_extract_data/<str:id>', manage_students_extract_data, name='manage_students_extract_data'),   
    path('/views_admin_panel_db_operations/manage_students_delete/<str:id>', manage_students_delete, name='manage_students_delete'),   


    path('/views_admin_panel_db_operations/manage_classes_add_student', manage_classes_add_student, name='manage_classes_add_student'),   
    path('/views_admin_panel_db_operations/manage_classes_deattach_subject', manage_classes_deattach_subject, name='manage_classes_deattach_subject'),   
    path('/views_admin_panel_db_operations/manage_classes_attach_subject', manage_classes_attach_subject, name='manage_classes_attach_subject'),   
    path('/views_admin_panel_db_operations/manage_classes_remove_student/', manage_classes_remove_student, name='manage_classes_remove_student'),   




    path('/views_admin_panel_db_operations/manage_subjects/', manage_subjects, name='manage_subjects'),   
    path('/views_admin_panel_db_operations/manage_subjects_add/', manage_subjects_add, name='manage_subjects_add'),   
    path('/views_admin_panel_db_operations/manage_subjects_attach_subject/', manage_subjects_attach_subject, name='manage_subjects_attach_subject'),   
    path('/views_admin_panel_db_operations/manage_subjects_remove_subject/', manage_subjects_remove_subject, name='manage_subjects_remove_subject'),   
    path('/views_admin_panel_db_operations/manage_subjects_fetch_standard_subjects/', manage_subjects_fetch_standard_subjects, name='manage_subjects_fetch_standard_subjects'),   

   
   
   
    path('/views_admin_panel_db_operations/manage_student/<str:uid>', manage_student, name='manage_student'),   
    path('/views_admin_panel_db_operations/manage_students_remove_class_from_profile/', manage_students_remove_class_from_profile, name='manage_students_remove_class_from_profile'),   
    path('/views_admin_panel_db_operations/manage_students_remove_subject_from_profile/', manage_students_remove_subject_from_profile, name='manage_students_remove_subject_from_profile'),   
    path('/views_admin_panel_db_operations/manage_students_attach_subject_to_profile/', manage_students_attach_subject_to_profile, name='manage_students_attach_subject_to_profile'),   
    
    
    
    path('/views_admin_panel_db_operations/manage_reports/', manage_reports, name='manage_reports'),   
    path('/views_admin_panel_db_operations/manage_reports/generate_absent_report', generate_absent_report, name='generate_absent_report'),   
    path('/views_admin_panel_db_operations/manage_reports/generate_attendance_report', generate_attendance_report, name='generate_attendance_report'),   
    path('/views_admin_panel_db_operations/manage_reports/generate_weekly_report', generate_weekly_report, name='generate_weekly_report'),   
   
   
    path('/views_admin_panel_db_operations/manage_reports/download_db', download_db, name='download_db'),   
    path('/views_admin_panel_db_operations/manage_reports/download_bak/<str:filename>', download_bak, name='download_db'),   



    



    # path('/waiting_list_teachers_list_update', waiting_list_teachers_list_update, name='waiting_list_teachers_list_update'),          






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

