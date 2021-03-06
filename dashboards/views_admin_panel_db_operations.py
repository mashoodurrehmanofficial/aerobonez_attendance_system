from django.conf.urls import include
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.http import  JsonResponse, response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from root.models import *
from django.shortcuts import render,redirect,HttpResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse,FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os,pandas as pd,uuid
from django.db.models import Q
from datetime import datetime
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
try:from .report_generator import *
except:from report_generator import *
# Create your views here.
import dateparser,time
from datetime import datetime
from dateutil import parser



def manage_standards(request): 
    standards = Standard.objects.all()
    return render(request, 'dashboards/manage_standards.html',{"standards":standards})
 


def manage_subjects(request): 
    standards = Standard.objects.all()
    return render(request, 'dashboards/manage_subjects.html',{"standards":standards})


def manage_subjects_fetch_standard_subjects(request):
    incoming_standard = request.GET["standard"] 
    subjects = list(Subject.objects.filter(standard__name=incoming_standard).order_by('name').values()) 
    other_subjects = list(Subject.objects.filter(~Q(standard__name=incoming_standard)).order_by('name').values())
     
    return JsonResponse({"subjects":subjects,'other_subjects':other_subjects})


def manage_subjects_add(request):
    incoming_standard = request.GET["standard"] 
    incoming_subject = request.GET["subject"]  
    if Subject.objects.filter(name=incoming_subject).exists():
        return JsonResponse({"error":f"Given Subject {incoming_subject}  already exists !"})
    else:
        Subject(name=incoming_subject).save()
        return JsonResponse({})


def manage_subjects_attach_subject(request):
    incoming_standard = request.GET["standard"] 
    incoming_subject = request.GET["subject"]  
    standard = Standard.objects.filter(name=incoming_standard).first()
    subject = Subject.objects.filter(name=incoming_subject).first()
    standard.subject_list.add(subject)
    response = manage_subjects_fetch_standard_subjects(request) 
    return response

 
def manage_subjects_remove_subject(request):
    incoming_standard = request.GET["standard"] 
    incoming_subject_id = request.GET["subject_id"] 
    standard = Standard.objects.filter(name=incoming_standard).first()
    subject = Subject.objects.filter(id=incoming_subject_id).first()
    standard.subject_list.remove(subject)
    response = manage_subjects_fetch_standard_subjects(request) 
    return response


def manage_standards_add(request): 
    incoming_standard = request.GET['standard']
    if Standard.objects.filter(name=incoming_standard).exists():pass
    else:Standard(name=incoming_standard).save()
    return JsonResponse({})


def manage_standards_delete(request,id): 
    Standard.objects.get(id=id).delete()
    return redirect("manage_standards")


def manage_classes(request): 
    standards = Standard.objects.all()
    classes = ClassList.objects.all()
    return render(request, 'dashboards/manage_classes.html',{"standards":standards,'classes':classes})



def get_class_students(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class']
    students = Student.objects.filter(classlist__name=incoming_class,classlist__uid=incoming_standard).order_by('name')
    students = [[x.name,x.id] for index,x in enumerate(students)]
    other_students = Student.objects.filter(~Q(classlist__name=incoming_class,classlist__uid=incoming_standard)).order_by('name')
    other_students = [[x.name,x.id] for index,x in enumerate(other_students)]
    
    
    subjects = Subject.objects.filter(standard__name=incoming_standard)
    subjects = [x.name for x in subjects]
    print("subjects -------------")
    print(subjects)



    return JsonResponse({'students':students,'other_students':other_students,'subjects':subjects})


def manage_classes_add(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class'] 
    ClassList(name=incoming_class,uid=incoming_standard).save()
    Standard.objects.get(name=incoming_standard).class_list.add(ClassList.objects.get(name=incoming_class,uid=incoming_standard))
    return JsonResponse({})


def manage_classes_delete(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class'] 
    ClassList.objects.filter(name=incoming_class,uid=incoming_standard).delete()

   
    return JsonResponse({})



def manage_student(request,uid): 
    student = Student.objects.get(uid=uid)
    return render(request, 'dashboards/manage_student_extract_data.html',{"student":student})


def manage_classes_add_student(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class']  
    incoming_id = request.GET['student_id'] 
    target_class = ClassList.objects.get(uid=incoming_standard,name=incoming_class) 
    student = Student.objects.get(id=incoming_id)
    target_class.student.add(student) 
    print("-->> Newly added student", student)
    students = Student.objects.filter(classlist__name=incoming_class,classlist__uid=incoming_standard).order_by('name')
    students = [[x.name,x.id,index+1] for index,x in enumerate(students)]
    other_students = Student.objects.filter(~Q(classlist__name=incoming_class,classlist__uid=incoming_standard)).order_by('name')
    other_students = [[x.name,x.id] for index,x in enumerate(other_students)]
    return JsonResponse({"students":students,'other_students':other_students})


def manage_classes_deattach_subject(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class_name']  
    incoming_subject = request.GET['subject']   
    target_records = Student_Subject_Model.objects.filter(
        subject=Subject.objects.get(name=incoming_subject),
        standard_name=incoming_standard,
        class_name=incoming_class,
    ) 
    try:target_records.delete()
    except :pass
    return JsonResponse({})



def manage_classes_attach_subject(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class_name']  
    incoming_subject = request.GET['subject']   
    students = Student.objects.filter(classlist__name=incoming_class,classlist__uid=incoming_standard)
    records = [
        student for student in students if not Student_Subject_Model.objects.filter(
            student=student,
            subject=Subject.objects.get(name=incoming_subject),
            standard_name=incoming_standard,
            class_name=incoming_class,
        ).exists()
    ]
    
    try:
        Student_Subject_Model.objects.bulk_create(
            [Student_Subject_Model(
                student=x,
                subject=Subject.objects.get(name=incoming_subject),
                standard_name=incoming_standard,
                class_name=incoming_class,
            ) for x in records]
        )
    except:pass
    return JsonResponse({})









def manage_classes_remove_student(request): 
    incoming_standard = request.GET['standard']
    incoming_class = request.GET['class']  
    incoming_id = request.GET['student_id'] 
    target_class = ClassList.objects.get(uid=incoming_standard,name=incoming_class) 
    student = Student.objects.get(id=incoming_id)
    target_class.student.remove(student) 
    print("-->> Removed student", student)
    students = Student.objects.filter(classlist__name=incoming_class,classlist__uid=incoming_standard).order_by('name')
    students = [[x.name,x.id,index+1] for index,x in enumerate(students)]
    other_students = Student.objects.filter(~Q(classlist__name=incoming_class,classlist__uid=incoming_standard)).order_by('name')
    other_students = [[x.name,x.id] for index,x in enumerate(other_students)]
    
    return JsonResponse({"students":students,'other_students':other_students})


def manage_students(request): 
    students = Student.objects.all()
    return render(request, 'dashboards/manage_students.html',{"students":students})

def manage_students_delete(request,id): 
    Student.objects.get(id=id).delete()
    return redirect('manage_students')

def manage_students_add(request):  
    incoming_student_name = request.GET['student_name']
    incoming_uid = request.GET['student_uid']
    if Student.objects.filter(name=incoming_student_name).exists() :
        return JsonResponse({"error":"Student name must be unique"})
    elif Student.objects.filter(uid=incoming_uid).exists() :
        return JsonResponse({"error":"Student ID must be unique"})
    else:
        Student(name=incoming_student_name,uid=incoming_uid).save()
        return JsonResponse({})


def manage_students_extract_data(request,id): 
    student = Student.objects.get(id=id)
    enrolled_classes = ClassList.objects.filter(student=student)

    enrolled_subjects = Student_Subject_Model.objects.filter(student=student)
    enrolled_subjects = [x.subject.name for x in  enrolled_subjects]

    enrolled_standard = Standard.objects.filter(class_list=ClassList.objects.filter(student=student).first()).first()
    other_subjects = Subject.objects.filter(~Q(name__in=enrolled_subjects),standard__name=enrolled_standard)

    return render(request, 'dashboards/manage_student_extract_data.html',{
        "student":student,
        'enrolled_classes':enrolled_classes,
        'enrolled_subjects':enrolled_subjects,
        'other_subjects':other_subjects,
        'enrolled_standard':enrolled_standard,
    })



def manage_students_remove_class_from_profile(request): 
    incoming_standard = request.GET['standard']
    class_name = request.GET['class_name']
    student_id = request.GET['student_id']
    student = Student.objects.get(id=student_id)
    target_class = ClassList.objects.filter(standard__name=incoming_standard,name=class_name).first()
    target_class.student.remove(student)

    Student_Subject_Model.objects.filter(class_name=class_name,standard_name=incoming_standard).delete()
    

    return JsonResponse({})



def manage_students_remove_subject_from_profile(request): 
    incoming_subject = request.GET['subject'] 
    student_id = request.GET['student_id']
    student = Student.objects.get(id=student_id)
    target_record = Student_Subject_Model.objects.filter(subject__name=incoming_subject,student=student).first()
    target_record.delete()
    return JsonResponse({})




def manage_students_attach_subject_to_profile(request): 
    incoming_subject = request.GET['subject'] 
    incoming_standard = request.GET['standard'] 
    student_id = request.GET['student_id']
    student = Student.objects.get(id=student_id)
    incmoing_class = class_list=ClassList.objects.filter(student=student).first()
    Student_Subject_Model(
        student = student,
        subject = Subject.objects.filter(name=incoming_subject).first(),
        class_name=incmoing_class,
        standard_name = incoming_standard
    ).save()
    return JsonResponse({})




def manage_students_filter_by_name(request): 
    query = request.GET['query'].strip()
    students = list(Student.objects.filter(name__startswith=query).values('id')) 

    if query=='empty_search_box':
        print("empty")
        students = list(Student.objects.all().values('id'))
    return JsonResponse({"students":students})






def manage_teachers_allow_teachers(request): 
    if request.user.is_superuser:
        waiting_list_teachers = TeacherProfile.objects.all().order_by('is_allowed')
        data = {
            'waiting_list_teachers':waiting_list_teachers
        }
        return render(request, 'dashboards/manage_teachers_allow_teachers.html',data)
    else:
        return redirect('/')

  
def manage_teachers_allow_teachers_post(request): 
    incoming_list = request.GET['teachers'].split(',')
    TeacherProfile.objects.filter(uid__in=incoming_list).update(is_allowed=True)
    TeacherProfile.objects.exclude(uid__in=incoming_list).update(is_allowed=False)
    Teacher.objects.filter(uid__in=incoming_list).update(is_allowed=True)
    Teacher.objects.exclude(uid__in=incoming_list).update(is_allowed=False)
    return JsonResponse({"message":True})


def manage_teachers(request): 
    teachers = Teacher.objects.all().order_by('name')
    return render(request, 'dashboards/manage_teachers.html',{"teachers":teachers})


def manage_teachers_add(request):  
    teacher_name = request.GET['teacher_name'] 
    if Teacher.objects.filter(name=teacher_name).exists() :
        return JsonResponse({"error":"Teacher name must be unique"}) 
    else: 
        Teacher(name=teacher_name).save()
        return JsonResponse({})


def manage_teachers_delete(request,id):  
    target_teacher = Teacher.objects.get(id=id) 
    target_teacher_account = User.objects.filter(username=target_teacher)
    if target_teacher_account.exists():target_teacher_account.delete()
    target_teacher.delete()
    print('Teacher data DELETED -> ', target_teacher  ,target_teacher_account)
    return redirect('manage_teachers')


def manage_teachers_extract_data(request,id):  
    target_teacher = Teacher.objects.get(id=id) 
    teacher_profile = TeacherProfile.objects.filter(name=target_teacher).first() 

    if request.method=='POST':
        new_teacher_name = request.POST['name']
        new_teacher_email = request.POST['email']
        new_teacher_password = request.POST['password']
        is_allowed = True if 'is_allowed' in request.POST.keys() else False
        teacher_id = request.POST['teacher_id']
        target_teacher = Teacher.objects.get(id=teacher_id)
        target_teacher_name = Teacher.objects.get(id=teacher_id).name
        target_teacher_profile = TeacherProfile.objects.get(name=target_teacher_name)
        target_user = User.objects.filter(email=target_teacher_profile.email).first()
        target_user.set_password(new_teacher_password)


        target_teacher_profile.is_allowed = is_allowed
        target_teacher_profile.password   = new_teacher_password
        target_teacher.is_allowed         = is_allowed
        is_admin = User.objects.filter(email=new_teacher_email)
        if is_admin:
            if is_admin.first().is_superuser:
                return render(request, 'dashboards/manage_teachers_extract_data.html',{
                "teacher_profile":teacher_profile,
                "teacher_id":id,
                'error': "Use some other email !!"
            })


        other_teacher_users = User.objects.filter(email=new_teacher_email)
        other_teacher_profile = TeacherProfile.objects.filter(email=new_teacher_email)


        if other_teacher_users.exists():
            if other_teacher_profile.first().uid!=target_teacher.uid:
                print("** collision detected !!")
                print("** error !!")
                return render(request, 'dashboards/manage_teachers_extract_data.html',{
                "teacher_profile":teacher_profile,
                "teacher_id":id,
                'error': f"This email address is already assigned to {other_teacher_users.first().username}"
            })
            else:
                print("updating email")
                target_teacher_profile.email = new_teacher_email
                target_user.email            = new_teacher_email
        else:
            print("++ updating email")
            target_teacher_profile.email = new_teacher_email
            target_user.email            = new_teacher_email 
        

  
        target_user.save()
        target_teacher.save()
        target_teacher_profile.save() 









        return redirect('manage_teachers_extract_data',id=id)
    else:
        return render(request, 'dashboards/manage_teachers_extract_data.html',{
            "teacher_profile":teacher_profile,
            "teacher_id":id
            
        })
        


def manage_reports(request):
    return render(request, 'dashboards/manage_reports.html')


def generate_absent_report(request,absent_report_date): 
    reports_folder = os.path.join(os.getcwd(),'Reports')
    if not os.path.exists(reports_folder):os.makedirs(reports_folder)
 
  
    absent_report_date = parser.parse(absent_report_date).date()
    print(absent_report_date) 
    return absent_report_generator(absent_report_date)

def generate_attendance_report(request,daily_report_date): 
    daily_report_date = parser.parse(daily_report_date).date()
    return attendance_report_generator(daily_report_date)

 


def generate_weekly_report(request,start_date,end_date): 
    start_date = parser.parse(start_date).date()
    end_date = parser.parse(end_date).date()
    time_start_date = time.mktime(start_date.timetuple())
    time_end_date = time.mktime(end_date.timetuple())
    if time_end_date>time_start_date:
        return weekly_report_generator(start_date,end_date)
    else:
        return HttpResponse("<h2>Please use valid Date Range")
        

     
def generate_weekly_absent_report(request,start_date,end_date,red_zone): 
    start_date = parser.parse(start_date).date()
    end_date = parser.parse(end_date).date()
    time_start_date = time.mktime(start_date.timetuple())
    time_end_date = time.mktime(end_date.timetuple())
    if time_end_date>time_start_date: 
        return weekly_absent_report_generator(start_date,end_date,red_zone)
    else:
        return HttpResponse("<h2>Please use valid Date Range")
        

     






def download_db(request): 
    file_path = os.path.join(os.path.join(os.getcwd(),'db.sqlite3'))
    response = FileResponse(open(file_path, 'rb'))
    return response

def download_bak(request,filename): 
    file_path = os.path.join(os.path.join(os.getcwd(),filename))
    response = FileResponse(open(file_path, 'rb'))
    return response
