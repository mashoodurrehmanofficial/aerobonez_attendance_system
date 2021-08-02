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
 

# standard_class_studentname = os.path.join(os.getcwd(),'standard_class_studentname.csv')
# level_standard_subject = os.path.join(os.getcwd(),'level_standard_subject.csv')
# df = pd.read_csv(standard_class_studentname)[['Name','Class']].groupby('Class') .agg(pd.Series.tolist).values.tolist()



 
# Student.objects.all().delete()
# Student.objects.bulk_create(
#     [Student(name=record[-1],uid=record[0]) for record in df]
# )

# df = pd.read_csv(standard_class_studentname).values.tolist()
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



data = ['8994793p', '7595598p', '7593711p', '9834608a', '8625395a', '8994795l', '8994796p', '9376198l', '7892970p', '8424383p', '7612364p', '9198602p', '8761309p', '7908219p', '7892815p', '9418157p', '6053457p', '6032559p', '9448668p', '8669780p']
data = [[(x[:-1]),x[-1]] for x in data]
data2=[]
all_students = Student.objects.filter(uid__in=[x[0] for x in data])
for student in all_students:
    record = [x for x in data if student.uid==x[0]][0]
    record.insert(0,student.name) 
    if record[-1]=='p':record[-1] = 'Present'
    if record[-1]=='a':record[-1] = 'Absent'
    if record[-1]=='l':record[-1] = 'Late' 
    data2.append(record)
    print(record)

