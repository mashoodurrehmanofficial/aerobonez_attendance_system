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





def get_attendance_data(request): 
    data = list(AttendanceReport.objects.all().values())
    print(type(data))
    return JsonResponse({
        "data":data
    })



def get_teacher_data(request): 
    data = list(TeacherProfile.objects.all().values())
    print(type(data))
    return JsonResponse({
        "data":data
    })



def get_class_list(request): 
    data = list(ClassList.objects.all().values())
    print(type(data))
    return JsonResponse({
        "data":data
    })



def get_subject_list(request): 
    data = list(Subject.objects.all().values())
    print(type(data))
    return JsonResponse({
        "data":data
    })



 




   



 
 