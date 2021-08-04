from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.http import  JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from root.models import *
from django.shortcuts import render,redirect,HttpResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse,FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os,pandas as pd,uuid
from datetime import datetime

report_folder = os.path.join(os.getcwd(),'Attendance Report') 
def checkfolder():
    if os.path.exists(report_folder):pass
    else:os.makedirs(report_folder)

# Create your views here.

@login_required(login_url='/account/login')
def teacherpanel(request): 
    teacher = TeacherProfile.objects.get(name=request.user)
    return render(request, 'dashboards/teacherpanel.html',{"teacher":teacher})



def mark_attendance(request): 
    teacher = TeacherProfile.objects.get(name=request.user)
    standards = Standard.objects.all()
    standards = [x.name for x in standards]
    if request.method=='POST':
        print(request.POST)
        incoming_teacher = request.POST['teacher']
        incoming_standard = request.POST['standard']
        incoming_class = request.POST['class']
        incoming_subject = request.POST['subject'] 
        students = Student.objects.filter(classlist__name=incoming_class,classlist__uid=incoming_standard).order_by('name')
        students = [[x.name,x.uid,index+1] for index,x in enumerate(students)]
        ids = [int(x[-1]) for x in students]
        print(students) 
        return render(request, 'dashboards/attendance_sheet.html',{
            'students':students,'ids':ids,'teacher':incoming_teacher,'standard':incoming_standard,
            'class':incoming_class,'subject':incoming_subject,'teacher':teacher
        })
    return render(request, 'dashboards/mark_attendance.html',{"teacher":teacher,'standards':standards})



def submit_attendance_sheet(request):
    teachers = Teacher.objects.all()
    if request.method=='POST':
        data = request.POST['data'].split(',')
        incoming_teacher = request.POST['teacher']
        incoming_standard = request.POST['standard']
        incoming_class = request.POST['class']
        incoming_subject = request.POST['subject']       
        data = [[(x[:-1]),x[-1]] for x in data]
        data_set=[]
        all_students = Student.objects.filter(uid__in=[x[0] for x in data])
        teacher_uid = TeacherProfile.objects.get(user=request.user).uid
        report_uid = str(uuid.uuid4())
        for index,student in enumerate(all_students):
            record = [x for x in data if student.uid==x[0]][0]
            record.insert(0,student.name) 
            if record[-1]=='p':record[-1] = 'Present'
            if record[-1]=='a':record[-1] = 'Absent'
            if record[-1]=='l':record[-1] = 'Late' 
            additional=[incoming_teacher,incoming_standard,incoming_class,incoming_subject]
            record= [report_uid]+ [teacher_uid]+ additional+ [student.uid] +[record[0],record[-1]]
            data_set.append(record)
            print(record)
        submit_time = str(datetime.now().strftime("%m-%d-%Y  %H-%M-%S"))
        AttendanceReport.objects.bulk_create(
            [AttendanceReport(
                    report_uid           = x[0],
                    teacher_uid          = x[1],
                    teacher_name         = x[2],
                    standard             = x[3],
                    class_name           = x[4],
                    subject              = x[5],
                    student_secret_id    = x[6],
                    student_name         = x[7],
                    attendance_status    = x[8],
                    submit_time          = submit_time
            ) for x in data_set]
        )
        return redirect('teacherpanel')



def view_attendance_directory(requset):
    teacher = TeacherProfile.objects.get(user=requset.user)
    teacher_reports = AttendanceReport.objects.filter(teacher_uid=teacher.uid).distinct()
    report_uids = list(set([x.report_uid for x in teacher_reports]))
    teacher_reports = [AttendanceReport.objects.filter(report_uid=x).first() for x in report_uids]
    return render(requset, "dashboards/view_attendance_directory.html",{'teacher':teacher,'teacher_reports':teacher_reports})



def load_attendance_sheet(request, report_uid):
    if request.method=='POST':
        data = request.POST['data'].split(',')    
        data = [[(x[:-1]),x[-1]] for x in data]
        for record in data:
            if record[-1]=='p':record[-1] = 'Present'
            if record[-1]=='a':record[-1] = 'Absent'
            if record[-1]=='l':record[-1] = 'Late' 
        
        
        target_records_in_db = AttendanceReport.objects.filter(report_uid=report_uid)
        for target_record in target_records_in_db:
            temp_record = [x for x in data if x[0]==target_record.student_secret_id][0]
            if temp_record:
                target_record.attendance_status = temp_record[-1]
                target_record.save()

    students = AttendanceReport.objects.filter(report_uid=report_uid)
    students = [[x.student_name,x.student_secret_id,x.attendance_status] for x in students] 
    teacher = TeacherProfile.objects.get(user=request.user)
    return render(request, "dashboards/update_attendance_sheet.html",{
        'report_uid':report_uid,'students':students,'teacher':teacher
        })






    
def get_classes(request):
    current_standard = Standard.objects.get(name=request.GET['standard'])
    classes = current_standard.class_list
    classes = ClassList.objects.filter(standard__name=current_standard)
    classes = [x.name for x in classes]
    print(classes)
    return JsonResponse({'classes':classes})
    
def get_subjects(request):
    standard = request.GET['standard']
    incoming_class = request.GET['class']
    print(standard)
    current_standard = Standard.objects.get(name=standard)
    subjects = Subject.objects.filter(standard__name=current_standard)
    subjects = [x.name for x in subjects]
    print(subjects)
    return JsonResponse({'subjects':subjects})
    
























@login_required(login_url='/account/login') 
def adminpanel(request): 
    if request.user.is_superuser:
        waiting_list_teachers = TeacherProfile.objects.all()
        data = {
            'waiting_list_teachers':waiting_list_teachers
        }
        return render(request, 'dashboards/adminpanel.html',data)
    else:
        return redirect('/')











  
def waiting_list_teachers_list_update(request): 
    incoming_list = request.GET['teachers'].split(',')
    TeacherProfile.objects.filter(uid__in=incoming_list).update(is_allowed=True)
    TeacherProfile.objects.exclude(uid__in=incoming_list).update(is_allowed=False)
    Teacher.objects.filter(uid__in=incoming_list).update(is_allowed=True)
    Teacher.objects.exclude(uid__in=incoming_list).update(is_allowed=False)
    return JsonResponse({"message":True})

 