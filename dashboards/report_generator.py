import os,shutil
import os,sys,django,pandas as pd
from numpy.core.fromnumeric import ptp
sys.path.append( os.path.join(os.path.dirname(__file__), 'PROJECT'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROJECT.settings")
django.setup()
from root.models import *
from itertools import chain
import random,uuid
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse,HttpResponse
from wsgiref.util import FileWrapper

reports_folder = os.path.join(os.getcwd(),'Reports')
if not os.path.exists(reports_folder):os.makedirs(reports_folder)
 
from datetime import datetime,timedelta

def absent_report_generator():
    today = str(datetime.now().strftime("%m-%d-%Y"))  
    data  = AttendanceReport.objects.filter(submit_time__startswith=today).order_by('standard')
    absent_report_data =[]
    headers = ['Standard','Class','Subject','Unique ID','Name','Attendance Status' ,'Parent1','Relation1','Telephone1','Parent2','Relation2','Telephone2','House number']
    for record in data:
        if record.attendance_status == 'Absent':
            target_student = Student.objects.get(uid=record.student_secret_id)
            new_record = [
                record.standard,
                record.class_name,
                record.subject,
                record.student_secret_id,
                record.student_name,
                record.attendance_status,
                target_student.parent1,
                target_student.relation1,
                target_student.telephone1,
                target_student.parent2,
                target_student.relation2,
                target_student.telephone2,
                target_student.house_number
            ]
            absent_report_data.append(new_record)
    df = pd.DataFrame(data=absent_report_data,columns=headers)
    file_name = 'Absent report data '+str(datetime.now().strftime("%m-%d-%Y  %H-%M-%S"))+'.csv'
    file = os.path.join(reports_folder,file_name)
    df.to_csv(file,index=False) 

    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
    shutil.rmtree(reports_folder)
    return response



def attendance_report_generator():
    today = str(datetime.now().strftime("%m-%d-%Y")) 
    data  = AttendanceReport.objects.filter(submit_time__startswith=today).order_by('standard')
    headers = ['Standard','Teacher name','Class','Subject','Total students','Present students','Percentage %']

    standards = Standard.objects.all()
    main_df_container=[]
    standards = list(sorted(set([x.standard for x in data])) ) 
    for standard in standards[:]:
        standard_df_container=[]
        standard_data = [x for x in data if str(standard)==x.standard]
        classes_in_standard = ClassList.objects.filter(standard__name=standard)
        for class_name in classes_in_standard:
            students_in_class = Student.objects.filter(classlist__name = class_name.name,classlist__uid = class_name.uid)
            total_students_in_class = len(students_in_class) 
            attended_subjects_of_today_in_class = data.filter(standard=standard,class_name=class_name.name)
            
            teacher_name = attended_subjects_of_today_in_class.first()
            if teacher_name:teacher_name=teacher_name.teacher_name.split('- ')[0]

            attended_subjects_of_today_in_class = list(set([x.subject for x in attended_subjects_of_today_in_class]))
            for attended_subject in attended_subjects_of_today_in_class:
                presents_in_subject_class = data.filter(standard=standard,class_name=class_name.name,subject=attended_subject,attendance_status= 'Present')
                total_presents_in_subject_class = len(presents_in_subject_class)
                percentage = str(round((total_presents_in_subject_class/total_students_in_class)*100,2))+' %'

                total_school_students = len(Student.objects.all())
                total_present_school_students = len(data.filter(attendance_status= 'Present'))
                overall_school_percentage = str(round((total_present_school_students/total_school_students)*100,2))+' %'

                record = [standard,teacher_name,class_name.name,attended_subject,total_students_in_class,total_presents_in_subject_class,percentage]
                standard_df_container.append(record)
                
        df = pd.DataFrame(data=standard_df_container,columns=headers)
        main_df_container.append(df)



    file_name = 'Attendance Report '+str(datetime.now().strftime("%m-%d-%Y  %H-%M-%S"))+'.xlsx'
    file = os.path.join(reports_folder,file_name)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    for index,df in enumerate(main_df_container):
        df.to_excel(writer, sheet_name=str(standards[index]),index=False)
    writer.save() 
    # writer
    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
    shutil.rmtree(reports_folder)
    return response