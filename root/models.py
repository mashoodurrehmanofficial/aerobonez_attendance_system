from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver





class Teacher(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    uid=models.CharField(max_length=200,default='',blank=True)  
    is_allowed = models.BooleanField(default=False)
    def __str__(self):
        return self.name




class  TeacherProfile(models.Model):
    email = models.CharField(max_length=1000, default='', blank=True)
    password = models.CharField(max_length=1000, default='', blank=True)
    name = models.CharField(max_length=1000, default='', blank=True)
    uid=models.CharField(max_length=200,default='',blank=True)  
    is_allowed = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    reset_code = models.CharField(max_length=1000, default='', blank=True)
    def __str__(self):
            return self.name


@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, *args, **kwargs):
    target_profile = TeacherProfile.objects.filter(email=instance.email).first()
    if target_profile:
        teacher = Teacher.objects.filter(name=target_profile.name).first()
        print('---',teacher)
        teacher.is_allowed = False
        teacher.save()
        target_profile.delete()
    else:
        print("fail")
        print(instance.email)




class Student(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    uid = models.CharField(max_length=1000, default='', blank=True) 
    is_allowed = models.BooleanField(default=False)
    parent1 = models.CharField(max_length=1000, default='', blank=True,unique=False)
    relation1 = models.CharField(max_length=1000, default='', blank=True,unique=False)
    telephone1 = models.CharField(max_length=1000, default='', blank=True,unique=False)
    parent2 = models.CharField(max_length=1000, default='', blank=True,unique=False)
    relation2 = models.CharField(max_length=1000, default='', blank=True,unique=False)
    telephone2 = models.CharField(max_length=1000, default='', blank=True,unique=False)
    house_number = models.CharField(max_length=1000, default='', blank=True,unique=False) 
    def __str__(self):
        return self.name
        


class ClassList(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    student = models.ManyToManyField(Student,blank=True)
    uid=models.CharField(max_length=200,default='',blank=True)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    
    def __str__(self):
        return self.name




class Standard(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    class_list = models.ManyToManyField(ClassList,blank=True)
    subject_list = models.ManyToManyField(Subject,blank=True)
    def __str__(self):
        return self.name








 
class AttendanceReport(models.Model):
    report_uid = models.CharField(max_length=100, default='',blank=True)
    normal_date = models.CharField(max_length=100, default='',blank=True)
    submit_time = models.CharField(max_length=100, default='',blank=True)
    submit_date_field = models.DateField(blank=True,default='')
    teacher_uid = models.CharField(max_length=100, default='',blank=True)
    teacher_name = models.CharField(max_length=300, default='',blank=True)
    standard = models.CharField(max_length=300, default='',blank=True)
    class_name = models.CharField(max_length=300, default='',blank=True)
    subject = models.CharField(max_length=300, default='',blank=True)
    student_secret_id = models.CharField(max_length=100, default='',blank=True)
    student_name = models.CharField(max_length=300, default='',blank=True) 
    attendance_status = models.CharField(max_length=10, default='',blank=True)
    def __str__(self):
        return str(self.teacher_name)+'__'+str(self.standard)+'__'+str(self.class_name)+'__'+str(self.subject)



class Student_Subject_Model(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    class_name =  models.CharField(max_length=100,blank=True,default='')
    standard_name =  models.CharField(max_length=100,blank=True,default='')
    def __str__(self):
        return str(self.student)+'__'+str(self.subject)