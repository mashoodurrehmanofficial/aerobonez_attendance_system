import os,shutil
import os,sys,django,pandas as pd 
sys.path.append( os.path.join(os.path.dirname(__file__), 'PROJECT'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROJECT.settings")
django.setup()
from root.models import *
from itertools import chain
import random,uuid
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse,HttpResponse
from wsgiref.util import FileWrapper
import dateparser
from datetime import datetime
from dateutil import parser

from django.db.models import Q
reports_folder = os.path.join(os.getcwd(),'Reports')

reports_folder = os.path.join(os.getcwd(),'Reports')
if not os.path.exists(reports_folder):os.makedirs(reports_folder)
  
def report_folder_generator():
    reports_folder = os.path.join(os.getcwd(),'Reports')
    if not os.path.exists(reports_folder):os.makedirs(reports_folder)
    

  

def absent_report_generator(absent_report_date):
    reports_folder = os.path.join(os.getcwd(),'Reports')
    shutil.rmtree(reports_folder)
    report_folder_generator()
    
    if not os.path.exists(reports_folder):os.makedirs(reports_folder)
 
  
    reports_folder = os.path.join(os.getcwd(),'Reports')
    if not os.path.exists(reports_folder):os.makedirs(reports_folder) 

    data  = AttendanceReport.objects.filter(submit_date_field=absent_report_date).order_by('standard')

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
    return response





def attendance_report_generator(daily_report_date):  
    reports_folder = os.path.join(os.getcwd(),'Reports')
    shutil.rmtree(reports_folder)
    report_folder_generator()
    if not os.path.exists(reports_folder):os.makedirs(reports_folder)
    # today_date_object =   parser.parse(str(datetime.now().date())).date() 

    
    data = AttendanceReport.objects.filter(submit_date_field=daily_report_date).order_by('standard')
    standards = Standard.objects.all() 
    main_df_container=[] 
    for standard in standards[:]:
        print("DF index = ", standard.name)
        standard_df_container=[]
        standard_data = data.filter(standard=standard.name) 
        classes_in_standard = ClassList.objects.filter(standard__name=standard)
        for class_name in classes_in_standard:
            subjects_in_class = Subject.objects.filter(standard__name=standard)
            total_students_in_class = Student.objects.filter(classlist__name = class_name.name,classlist__uid = class_name.uid).count()
            
            print("-->> Class index = ", class_name)
            for subject_in_class in subjects_in_class:
                print("------>> Subject index = ", subject_in_class)
                current_subject_class_data = standard_data.filter(class_name=class_name,subject=subject_in_class)
                students_in_subject_class = Student_Subject_Model.objects.filter(subject=subject_in_class,class_name=class_name.name,standard_name=class_name.uid)
                total_students_in_subject_class = students_in_subject_class.count()
                try:
                    x = students_in_subject_class.first().student.name
                    y = current_subject_class_data.filter(student_name=x).count()
                    if y==0:y=1 
                    present_students = round(current_subject_class_data.filter(~Q(attendance_status='Absent')).distinct().count()/y,2)
                    absent_students = round(current_subject_class_data.filter(attendance_status='Absent').distinct().count()/y,2)
                    percentage = round((present_students/total_students_in_subject_class)*100,2)
                except:
                    present_students = 'N/A'
                    absent_students = 'N/A'
                    percentage = 'N/A'
                    total_students_in_subject_class = 'N/A'
                if present_students==0:absent_students=total_students_in_subject_class
                try:teacher_name = current_subject_class_data.first().teacher_name
                except: teacher_name="No teacher marked attendance"
                record = [
                    standard.name,teacher_name,class_name.name,
                    subject_in_class.name,present_students,absent_students,percentage,
                    total_students_in_subject_class,total_students_in_class
                ]
                standard_df_container.append(record)
        df=pd.DataFrame(standard_df_container,columns=['Standard','Teacher','Class','Subject','Present','Absent','Percentage %','Total students in subjective-class', 'Overall students in class'])
        print(df)
        main_df_container.append(df)

                
            

    
    writer = pd.ExcelWriter('attendace_report.xlsx', engine='xlsxwriter')
    for index,df in enumerate(main_df_container):
        df.to_excel(writer, sheet_name=str(standards[index]),index=False)
    writer.save()


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
    # shutil.rmtree(reports_folder)
    return response


    
def weekly_absent_report_generator(start_date,end_date,red_zone): 
    # shutil.rmtree(reports_folder)
    shutil.rmtree(reports_folder)
    report_folder_generator()

    # start_date = parser.parse("September 01, 2021").date()
    # end_date = parser.parse("September 08, 2021").date()
    data = AttendanceReport.objects.filter(submit_date_field__range=[start_date,end_date]).order_by('standard').distinct()
    # red_zone = 40
    absent_report_data =[]
    students = Student.objects.all()
    for student in students[:]:
        total_classes_marked = data.filter(student_name=student.name)
        if total_classes_marked.exists():
            total_absents = total_classes_marked.filter(attendance_status="Absent").count()
            total_classes_marked = total_classes_marked.count()
            if total_absents==0:percentage = round(0,2)*100
            else:   
                percentage = (total_absents/total_classes_marked)*100
                percentage = round(percentage,2)
            if percentage>float(red_zone):
                new_record = [
                    student.name,
                    str(percentage)+ " % ",
                    str(red_zone)+ " % ",

                    student.parent1,
                    student.relation1,
                    student.telephone1,
                    student.parent2,
                    student.relation2,
                    student.telephone2,
                    student.house_number
                ]
                absent_report_data.append(new_record)
            print(f"{total_classes_marked} - {total_absents} = {total_classes_marked-total_absents} =>",  str(percentage)+ " % ")
            

    headers = ["Student Name","Absent Percentage","Maximum Limit",'Parent1','Relation1','Telephone1','Parent2','Relation2','Telephone2','House number']
    df = pd.DataFrame(data=absent_report_data,columns=headers)
    file_name = 'Weekly Absent report data '+str(datetime.now().strftime("%m-%d-%Y  %H-%M-%S"))+'.csv'
    file = os.path.join(reports_folder,file_name)
    df.to_csv(file,index=False) 
 
    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
    return response











def weekly_report_generator(start_date,end_date): 
    reports_folder = os.path.join(os.getcwd(),'Reports')
    shutil.rmtree(reports_folder)
    report_folder_generator()
    if not os.path.exists(reports_folder):os.makedirs(reports_folder)
    today_date_object =   parser.parse(str(datetime.now().date())).date()
    # start_date = parser.parse("August 23, 2021").date()
    # end_date = parser.parse("August 29, 2021").date()

    data = AttendanceReport.objects.filter(submit_date_field__range=[start_date,end_date]).order_by('standard')
    # data = AttendanceReport.objects.filter(submit_date_field=today_date_object).order_by('standard')


    standards = Standard.objects.all() 
    main_df_container=[] 
    for standard in standards[:]:
        print("DF index = ", standard.name)
        standard_df_container=[]
        standard_data = data.filter(standard=standard.name) 
        classes_in_standard = ClassList.objects.filter(standard__name=standard)
        for class_name in classes_in_standard:
            subjects_in_class = Subject.objects.filter(standard__name=standard)
            total_students_in_class = Student.objects.filter(classlist__name = class_name.name,classlist__uid = class_name.uid).count()
            
            print("-->> Class index = ", class_name)
            for subject_in_class in subjects_in_class:
                print("------>> Subject index = ", subject_in_class)
                current_subject_class_data = standard_data.filter(class_name=class_name,subject=subject_in_class)
                students_in_subject_class = Student_Subject_Model.objects.filter(subject=subject_in_class,class_name=class_name.name,standard_name=class_name.uid)
                total_students_in_subject_class = students_in_subject_class.count()
                try:
                    x = students_in_subject_class.first().student.name
                    y = current_subject_class_data.filter(student_name=x).count()
                    if y==0:y=1 
                    present_students = round(current_subject_class_data.filter(~Q(attendance_status='Absent')).distinct().count()/y,2)
                    absent_students = round(current_subject_class_data.filter(attendance_status='Absent').distinct().count()/y,2)
                    percentage = round((present_students/total_students_in_subject_class)*100,2)
                except:
                    present_students = 'N/A'
                    absent_students = 'N/A'
                    percentage = 'N/A'
                    total_students_in_subject_class = 'N/A'
                if present_students==0:absent_students=total_students_in_subject_class
                try:teacher_name = current_subject_class_data.first().teacher_name
                except: teacher_name="No teacher marked attendance"
                record = [
                    standard.name,teacher_name,class_name.name,
                    subject_in_class.name,present_students,absent_students,percentage,
                    total_students_in_subject_class,total_students_in_class
                ]
                standard_df_container.append(record)
        df=pd.DataFrame(standard_df_container,columns=['Standard','Teacher','Class','Subject','Present','Absent','Percentage %','Total students in subjective-class', 'Overall students in class'])
        print(df)
        main_df_container.append(df)

                
            

    
    writer = pd.ExcelWriter('attendace_report.xlsx', engine='xlsxwriter')
    for index,df in enumerate(main_df_container):
        df.to_excel(writer, sheet_name=str(standards[index]),index=False)
    writer.save()






    file_name = 'FridayReport '+str(datetime.now().strftime("%d-%m-%Y"))+'.xlsx'
    file = os.path.join(reports_folder,file_name)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    for index,df in enumerate(main_df_container):
        df.to_excel(writer, sheet_name=str(standards[index]),index=False)
    writer.save()
    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
    # shutil.rmtree(reports_folder)
    return response


