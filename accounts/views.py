from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

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
                return render(request, 'accounts/signup.html',{"teachers":teachers,"error":"Email already exists !"})
            else:
                user = User(username=usernmae,email=email,password=make_password(password))
                user.save()
                uid = uuid.uuid4()
                teacher = Teacher.objects.get(name=usernmae)
                teacher.uid=uid
                teacher.save()
                teacher_profile = TeacherProfile(name=usernmae,user=user,uid=uid)
                teacher_profile.save()
                return render(request, 'accounts/login.html',{"teachers":teachers,'message':"Account created successfully !"})
        except IntegrityError:
                return render(request, 'accounts/signup.html',{"teachers":teachers,"error":"Teacher name has already been selected !"})


    return render(request, 'accounts/signup.html',{"teachers":teachers})






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
                return render(request, 'accounts/login.html',{"error":"Sorry, email or password is incorrect !"})
        else:
            print("dont exists")
            return render(request, 'accounts/login.html',{"error":"Sorry, email or password is incorrect !"})
    return render(request, 'accounts/login.html')






def logout_page(request):
    logout(request)
    return redirect('login_page')