from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

try:from .EMAIL_SENDER import SEND_MESSAGE
except ImportError:from EMAIL_SENDER import SEND_MESSAGE

from root.models import *

# Create your views here.


def signup_page(request):
    teachers = Teacher.objects.filter(is_allowed=False)
    if request.method=='POST':
        usernmae = request.POST['usernmae']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        try:
            if user.exists():
                return render(request, 'accounts/signup.html',{"page_title":"Sign Up","teachers":teachers,"error":"Email already exists !"})
            else:
                user = User(username=usernmae,email=email,password=make_password(password))
                user.save()
                uid = uuid.uuid4()
                teacher = Teacher.objects.get(name=usernmae)
                teacher.uid=uid
                teacher.save()
                teacher_profile = TeacherProfile(name=usernmae,user=user,uid=uid,email=email,password=password)
                teacher_profile.save()
                return render(request, 'accounts/login.html',{"page_title":"Sign Up","teachers":teachers,'message':"Account created successfully !"})
        except IntegrityError:
                return render(request, 'accounts/signup.html',{"page_title":"Sign Up","teachers":teachers,"error":"Teacher name has already been selected !"})


    return render(request, 'accounts/signup.html',{"page_title":"Sign Up","teachers":teachers})






def login_page(request):
    if request.method=='POST':
        # usernmae = request.POST['usernmae']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            username = user.username
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                print("login successful !")
                if user.is_superuser:
                    return redirect('adminpanel')
                else:
                    return redirect('teacherpanel')
            else:
                return render(request, 'accounts/login.html',{"page_title":"Login","error":"Maaf, email ataupun Password tidak sah"})
        else:
            print("dont exists")
            return render(request, 'accounts/login.html',{"page_title":"Login","error":"Maaf, email ataupun Password tidak sah"})
    return render(request, 'accounts/login.html',{"page_title":"Login"})






def logout_page(request):
    logout(request)
    return redirect('login_page')



def message_page(request):
    return render(request,'accounts/message_page.html')




def message_page(request):
    return render(request,'accounts/message_page.html')

def forgot_password(request): 
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            target_profile = TeacherProfile.objects.filter(email=email).first()
            code = str(str(uuid.uuid4())+str(uuid.uuid4())).replace('-','')
            target_profile.reset_code = code
            target_profile.save() 
            SEND_MESSAGE(email,f"http://54.255.3.66:8000//account/reset_password/{code}")
            return redirect("message_page")
        else:
            return render(request, 'accounts/forgot_password.html',{"error":"Emael tersebut tidak wujud di database kami!"})
    return render(request,'accounts/forgot_password.html')





def reset_password(request,reset_code):
    target_profile = TeacherProfile.objects.filter(reset_code=reset_code).first()
    if target_profile:
            if request.method == 'POST':
                new_password = request.POST['password']
                target_user = User.objects.filter(email=target_profile.email).first()
                target_user.set_password(new_password)
                target_user.save()
                target_profile.password = new_password
                target_profile.reset_code = ''
                target_profile.save()
                print(target_user)
                return redirect('login_page')


            else:
                return render(request,'accounts/reset_password.html')
    else:
        return HttpResponse("<h1>Wrong Reset Link</h1>")