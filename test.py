import os,sys,django,pandas as pd
sys.path.append( os.path.join(os.path.dirname(__file__), 'PROJECT'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROJECT.settings")
django.setup()
from root.models import *
from itertools import chain
 

# teacher_file = os.path.join(os.getcwd(),'teacher_names.csv')
# teacher_df = pd.read_csv(teacher_file).values.tolist()


# Teacher.objects.all().delete()
# Teacher.objects.bulk_create(
#     [Teacher(name=name[0]) for name in teacher_df]
# )
 

standard_class_studentname = os.path.join(os.getcwd(),'standard_class_studentname.csv')
level_standard_subject = os.path.join(os.getcwd(),'level_standard_subject.csv')
# df = pd.read_csv(standard_class_studentname)[['Name','Class']].groupby('Class') .agg(pd.Series.tolist).values.tolist()



 
# Student.objects.all().delete()
# Student.objects.bulk_create(
#     [Student(name=record[-1],uid=record[0]) for record in df]
# )

df = pd.read_csv(standard_class_studentname).values.tolist()
# df = [[x[0],x[1],x[-1]] for x in df]
 
 
# classes = list(set([x[-1] for x in df]))
# cname = 'SEMARAK'
# ['MAWAR', 'MELATI', 'MELUR', 'CEMPAKA', 'SEMARAK', 'KEMBOJA', 'RAYA', 'ANGGERIK', 'TANJUNG', 'KENANGA', 'IXORA', 'SEROJA', 'TERATAI', 'MPV']

# students = [[x[0],x[1]] for x in df if x[-1]==cname]
# students = [Student.objects.get(uid=x[0],name=x[1]) for x in students]
# for cname in classes:
#     classindb = ClassList.objects.filter(name=cname) 
#     students = [[x[0],x[1]] for x in df if x[-1]==cname]
#     students = [Student.objects.get(uid=x[0],name=x[1]) for x in students]

#     if classindb.exists():
#         classindb = ClassList.objects.get(name=cname) 
#         classindb.student.add(*students)
#     else:
#         ClassList(name=cname).save()
#         classindb = ClassList.objects.get(name=cname)  
     



# for record in df:  
#     stdindb = Student.objects.get(uid=record[0],name=record[1])
#     cname = record[-1] 
#     classindb = ClassList.objects.filter(name=cname) 
#     if classindb.exists():
#         classindb = ClassList.objects.get(name=cname) 
#         classindb.student.add(stdindb)
#     else:
#         ClassList(name=cname).save()
#         classindb = ClassList.objects.get(name=cname)  
     



# Standard.objects.all().delete()
# Standard.objects.bulk_create(
#     [Standard(name=x) for x in standards]
# )


# df = pd.read_csv(level_standard_subject).values.tolist()
# subjects = list(chain.from_iterable(df))
# subjects = list(set([x for x in subjects if type(x) is str]))





# Subject.objects.all().delete()
# Subject.objects.bulk_create(
#     [Subject(name=x) for x in subjects]
# )
# df = pd.read_csv(level_standard_subject)
# standards = list(df.columns)
# for standard in standards:
#     subjects = df[standard].values.tolist()
#     subjects = list(set([x for x in subjects if type(x) is str]))
#     standard = Standard.objects.get(name=standard)
#     subjects = [Subject.objects.get(name=x) for x in subjects]
#     standard.subject_list.add(*subjects)




# df = pd.read_csv(standard_class_studentname)
# standards = list(set(df['Standard'].values.tolist()))
# for standard in standards:
#     classes = list(set([x[-1] for x in df.values.tolist() if x[2]==standard]))
#     classes = [ClassList.objects.get(name=x) for x in classes]
#     standard = Standard.objects.get(name=standard)
#     standard.class_list.add(*classes)




# df = pd.read_csv(standard_class_studentname).values.tolist()
# df = [[x[-1],x[-2]] for x in df]
# df = list(set(tuple(sorted(x)) for x in df))
# df = [list(x) for x in df]


# ClassList.objects.all().delete()
# ClassList.objects.bulk_create(
#     [ClassList(name=x[0],uid=x[-1]) for x in df]
# )




# df = pd.read_csv(standard_class_studentname).values.tolist()
# standards = list(set([x[-2] for x in df]))
# for standard in standards:
#     classes = list(set([x[-1] for x in df if x[-2]==standard]))
#     classes = [ClassList.objects.get(name=x,uid=standard) for x in classes]
#     standard = Standard.objects.get(name=standard)
#     standard.class_list.add(*classes)
#     print(standard)







# x = ClassList.objects.filter(uid='TINGKATAN 5')
# print(len(x.distinct()))




# df = pd.read_csv(standard_class_studentname).values.tolist()
# standards = list(set([x[-2] for x in df]))

# # [1727593, 'YUKI HEW YUN XIAN', 'TINGKATAN 5', 'CEMPAKA']
# students = Student.objects.all()

# for standard in standards:
#     classes = ClassList.objects.filter(uid=standard)
#     for target_class in classes:
#         students = [x[:2] for x in df if x[-1]==target_class.name]
#         students = [Student.objects.get(uid=x[0],name=x[-1]) for x in students]
#         if standard=='TINGKATAN 5' and target_class.name=='CEMPAKA':
#             print('-'*50)
#             print(([x.name for x in students]))
#         target_class.student.add(*students)
#         print('-'*50)
        
# students = Student.objects.filter(classlist__uid='TINGKATAN 5',classlist__name='CEMPAKA')
# print(len(students))






# df = pd.read_csv(standard_class_studentname).values.tolist()
# standards = list(set([x[-2] for x in df]))

# # # [1727593, 'YUKI HEW YUN XIAN', 'TINGKATAN 5', 'CEMPAKA']
# # students = Student.objects.all()
# for standard in standards:
#     classes = ClassList.objects.filter(uid=standard)
#     for target_class in classes:
#         newdf = pd.read_csv(standard_class_studentname).groupby(['Standard','Class']).get_group((standard,target_class.name)).agg(list).values.tolist()
#         students = [x[:2] for x in newdf]
#         students = [Student.objects.get(uid=x[0],name=x[-1]) for x in students]
#         print(students)
#         print(len(students))
#         target_class.student.add(*students)    
            
            
# x=(Student.objects.filter(classlist__name='CEMPAKA',classlist__uid='TINGKATAN 5'))

# print(len(x))