from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class MloginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email','password']

class ApplyForm(ModelForm):
    class Meta:
        model = Student
        exclude = ["user_id"]

class UpdateProfileForm(ModelForm):
    class Meta:
        model = Student
        exclude = ["user_id",'photo','contact']


class AddCourseForm(ModelForm):
    class Meta:
        model = StudentCourse
        exclude = ['user_id','data_of_join','status','course_name']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
