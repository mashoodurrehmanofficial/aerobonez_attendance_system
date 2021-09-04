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
from dateutil import parser
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse,HttpResponse
from wsgiref.util import FileWrapper

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
        incoming_teacher = request.POST['teacher']
        incoming_standard = request.POST['standard']
        incoming_class = request.POST['class']
        incoming_subject = request.POST['subject'] 

        students = Student_Subject_Model.objects.filter(
            subject__name=incoming_subject,standard_name=incoming_standard,class_name=incoming_class).order_by('student__name')
        
        students = [[x.student.name,x.student.uid] for x in students] 
        ids = [int(x[-1]) for x in students]
        return render(request, 'dashboards/attendance_sheet.html',{
            'students':students,'ids':ids,'teacher':incoming_teacher,'standard':incoming_standard,
            'class':incoming_class,'subject':incoming_subject,'teacher':teacher
        })
    return render(request, 'dashboards/mark_attendance.html',{"teacher":teacher,'standards':standards})



def submit_attendance_sheet(request):
    if request.method=='POST':
        data                = request.POST['data'].split(',')
        incoming_teacher    = request.POST['teacher']
        incoming_standard   = request.POST['standard']
        incoming_class      = request.POST['class']
        incoming_subject    = request.POST['subject']      
        incoming_date       = request.POST['date']      
        date_object = parser.parse(str(incoming_date)).date()
        
        data = [[(x[:-1]),x[-1]] for x in data]
        print(data)
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
        submit_time = str(datetime.now().strftime("%m-%d-%Y")) 
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
                    submit_time          = submit_time,
                    normal_date          = incoming_date,
                    submit_date_field    = date_object
            ) for x in data_set]
        )
        return redirect('teacherpanel')



def view_attendance_directory(requset):
    teacher = TeacherProfile.objects.get(user=requset.user)
    teacher_reports = AttendanceReport.objects.filter(teacher_uid=teacher.uid).distinct().order_by('-submit_date_field')
    report_uids = list(dict.fromkeys([x.report_uid for x in teacher_reports]))



    
    teacher_reports = [AttendanceReport.objects.filter(report_uid=x).first() for x in report_uids]
    return render(requset, "dashboards/view_attendance_directory.html",{'teacher':teacher,'teacher_reports':teacher_reports})



def load_attendance_sheet(request, report_uid):
    if request.method=='POST':
        data = request.POST['data'].split(',')   
        incoming_date       = request.POST['date'] 
        date_object = parser.parse(str(incoming_date)).date()
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
                target_record.submit_date_field = date_object 
                target_record.normal_date       = incoming_date 
                target_record.save()


    students = AttendanceReport.objects.filter(report_uid=report_uid)
    target_report = AttendanceReport.objects.filter(report_uid=report_uid).first()
    standard = target_report.standard
    subject = target_report.subject
    class_name = target_report.class_name


    normal_date = students.first().normal_date
    students = [[x.student_name,x.student_secret_id,x.attendance_status] for x in students] 
    teacher = TeacherProfile.objects.get(user=request.user)
    return render(request, "dashboards/update_attendance_sheet.html",{
        'report_uid':report_uid,'students':students,'teacher':teacher,'normal_date':normal_date,
        'standard':standard,
            'class':class_name,'subject':subject
        })


def pdf_attendance_sheet(request, report_uid):
    target_report = AttendanceReport.objects.filter(report_uid=report_uid).order_by('student_name')
    header = ['Standard','Class','Subject','Student Name','Status']
    data_set = [[x.standard,x.class_name,x.subject,x.student_name,x.attendance_status] for x in target_report]
    df = pd.DataFrame(data_set,columns=header)
    reports_folder = os.path.join(os.getcwd(),'Reports')
    if not os.path.exists(reports_folder):os.makedirs(reports_folder)
    standard = str(target_report.first().standard)
    subject = str(target_report.first().subject)
    class_name = str(target_report.first().class_name)
    file_name = standard+'_'+subject+'_'+class_name+'_'
    file_name =file_name+str(datetime.now().strftime("%m-%d-%Y  %H-%M-%S"))+'.xlsx'
    file = os.path.join(reports_folder,file_name)
    df.to_excel(file,index=False) 
    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
    return response
 
  
def delete_attendance_sheet(request, report_uid):
    target_report = AttendanceReport.objects.filter(report_uid=report_uid)
    target_report.delete()
    return redirect('view_attendance_directory') 
 
  
 


    
def get_classes(request):
    current_standard = Standard.objects.get(name=request.GET['standard'])
    classes = current_standard.class_list
    classes = ClassList.objects.filter(standard__name=current_standard)
    
    classes = [x.name for x in classes]
    

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

 




   



 
 