from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone

class Student(models.Model):
    DEGREE = (("BCA","BCA"),("BTECH","BTECH"),("BSc","BSc"),("MCA","MCA"),("OTHER","OTHER"))
    GENDER = (("M","Male"),("F","FEMALE"),("O","Other"))
    std_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    date_of_birth = models.CharField(max_length=200)
    degree = models.CharField(choices=DEGREE,max_length=200)
    address = models.TextField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="apply/image")
    gender = models.CharField(choices=GENDER,max_length=200)
    contact = models.IntegerField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default='0',choices=(("0","Pending"),("1","Active"),("2","Courseless"),("3","takeout")))
    slugs = models.SlugField(max_length=200)

    def __str__(self):
        return self.first_name


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_duration = models.CharField(max_length=200)
    course_fees = models.IntegerField()

    def __str__(self):
        return self.course_name


class StudentCourse(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    course_type = models.CharField(max_length=200,choices=(("1","COURSE"),("2","MONTHLY")))
    status = models.CharField(max_length=200,choices=(("1","ACTIVE"),("0","Closed")))
    data_of_join = models.DateField(default=timezone.now)

    def __str__(self):
        return self.course_name.course_name

class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    p_month = models.DateTimeField()
    p_amount = models.IntegerField()
    p_due = models.IntegerField()
    p_course = models.ForeignKey(StudentCourse,null=True,on_delete=models.DO_NOTHING)
    p_status = models.CharField(choices=(("0","Not paid"),("1","Pending"),("2","Paid")),max_length=200)
    user_id = models.ForeignKey(User,models.CASCADE)

    def __str__(self):
        return str(self.p_month)

