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




# # Create your views here.
# def attendance(request):
#     teachers = Teacher.objects.all()
#     if request.method=='POST':
#         data = request.POST['data'].split(',')
#         incoming_teacher = request.POST['teacher']
#         incoming_standard = request.POST['standard']
#         incoming_class = request.POST['class']
#         incoming_subject = request.POST['subject']       
#         data = [[(x[:-1]),x[-1]] for x in data]
#         data_set=[]
#         all_students = Student.objects.filter(uid__in=[x[0] for x in data])
#         for index,student in enumerate(all_students):
#             record = [x for x in data if student.uid==x[0]][0]
#             record.insert(0,student.name) 
#             if record[-1]=='p':record[-1] = 'Present'
#             if record[-1]=='a':record[-1] = 'Absent'
#             if record[-1]=='l':record[-1] = 'Late' 
#             additional=[incoming_teacher,incoming_standard,incoming_class,incoming_subject]
#             record= [index+1]+ additional+[record[0],record[-1]]
#             data_set.append(record)
#             print(record)
#         header = ['Index','Teacher','Standard','Class','Subject','Student Name','Attendance Status']
#         df = pd.DataFrame(data=data_set,columns=header)
#         checkfolder()
#         filename = str(datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))+'.csv'
#         file_path = os.path.join(report_folder,filename)
#         df.to_csv(file_path,index=False)


#         return render(request, 'root/completion.html',{'download_url':filename})
    
#     else:
#         return render(request, 'root/attendance.html')
    

def download(request, filename): 
    file_path = os.path.join(report_folder,filename)
    response = FileResponse(open(file_path, 'rb'))
    return response








# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    teachers = Teacher.objects.all()
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

        return render(request, 'root/attendance.html',{
            'students':students,'ids':ids,'teacher':incoming_teacher,'standard':incoming_standard,
            'class':incoming_class,'subject':incoming_subject
        })
    

    else:
        return render(request, 'root/index.html',{"page_title":'e-Hadir SMKBM','teachers':teachers})
    



 
 
 
 


# @csrf_exempt
# @login_required(login_url="loginuser") 