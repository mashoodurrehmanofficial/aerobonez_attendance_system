from django.db import models
from django.contrib.auth.models import User
import uuid


class Teacher(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    uid = models.CharField(max_length=1000, default='', blank=True) 

    def __str__(self):
        return self.name
        


class ClassList(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    student = models.ManyToManyField(Student,null=True,blank=True)
    uid=models.CharField(max_length=200,default='',blank=True)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    def __str__(self):
        return self.name




class Standard(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True)
    class_list = models.ManyToManyField(ClassList,null=True,blank=True)
    subject_list = models.ManyToManyField(Subject,null=True,blank=True)
    def __str__(self):
        return self.name








 
