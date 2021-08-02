from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse,FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os,pandas as pd
from datetime import datetime

report_folder = os.path.join(os.getcwd(),'Attendance Report') 
def checkfolder():
    if os.path.exists(report_folder):pass
    else:os.makedirs(report_folder)




# Create your views here.
def attendance(request):
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
        for student in all_students:
            record = [x for x in data if student.uid==x[0]][0]
            record.insert(0,student.name) 
            if record[-1]=='p':record[-1] = 'Present'
            if record[-1]=='a':record[-1] = 'Absent'
            if record[-1]=='l':record[-1] = 'Late' 
            additional=[incoming_teacher,incoming_standard,incoming_class,incoming_subject]
            record=additional+[record[0],record[-1]]
            data_set.append(record)
            print(record)

        header = ['Teacher','Standard','Class','Subject','Student Name','Attendance Status']
        df = pd.DataFrame(data=data_set,columns=header)
        checkfolder()
        filename = str(datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))+'.csv'
        file_path = os.path.join(report_folder,filename)
        df.to_csv(file_path,index=False)


        return render(request, 'root/completion.html',{'download_url':filename})
    
    else:
        return render(request, 'root/attendance.html')
    

def download(request, filename): 
    file_path = os.path.join(report_folder,filename)
    response = FileResponse(open(file_path, 'rb'))
    return response








# Create your views here.
def index(request):
    teachers = Teacher.objects.all()
    if request.method=='POST':
        print(request.POST)
        incoming_teacher = request.POST['teacher']
        incoming_standard = request.POST['standard']
        incoming_class = request.POST['class']
        incoming_subject = request.POST['subject']  
        target_class = ClassList.objects.filter(standard__name= Standard.objects.get(name=incoming_standard)).filter(name=incoming_class).first()
        students = Student.objects.filter(classlist__name=target_class).order_by('name')
        students = [[x.name,x.uid] for x in students]
        ids = [int(x[-1]) for x in students]
        print(students)

        return render(request, 'root/attendance.html',{
            'students':students,'ids':ids,'teacher':incoming_teacher,'standard':incoming_standard,
            'class':incoming_class,'subject':incoming_subject
        })
    

    else:
        return render(request, 'root/index.html',{'teachers':teachers})
    



def get_standards(request):
    standards = Standard.objects.all()
    standards = [x.name for x in standards]
    print(standards)
    return JsonResponse({'standards':standards})
    

 
 


    
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
    

 
 


# @csrf_exempt
# @login_required(login_url="loginuser") 