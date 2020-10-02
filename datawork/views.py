from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from datedelta import datedelta
from django.contrib.auth import authenticate,login
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from datetime import timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
import calendar

def send_sms(number,msg):
    import http.client
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"%s\", \"to\":[\"%d\"] } ] }" % (msg,number)
    print(payload)
    headers = {
        'authkey': "255108A7ZoapPO5c93a8ca",
        'content-type': "application/json"
    }
    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def home(r):
    data = {}
    return render(r,'home.html',data)

def about(r):
    data = {}
    return render(r,'about.html',data)

def course(r):
    data = {"stdcourse": StudentCourse.objects.filter(user_id__username=r.user),}
    return render(r,'course.html',data)

def contact(r):
    data = {}
    return render(r,'contact.html',data)

def register(r):
    u = UserCreationForm(r.POST or None)
    if r.method=="POST":
        if u.is_valid():
            u.save()
            a = authenticate(username=r.POST.get('username'),password=r.POST.get('password1'))
            login(r,a)
            return redirect('apply')

    data = {"form":u}
    return render(r, 'registration/register.html', data)


@login_required()
def apply(r):
    a = ApplyForm(r.POST or None, r.FILES or None)
    if r.method == "POST":
        if a.is_valid():
            d = a.save(commit=False)
            user = User.objects.get(username=r.user)
            d.user_id = user
            d.save()
            return redirect('student_profile')
    data = {"form":a}
    return render(r,'apply.html',data)

def mlogin(r):
    mu = MloginForm(r.POST or None)
    if r.method == 'POST':
        if mu.is_valid:
            email = r.POST['email']
            password = r.POST['password']
            username = User.objects.get(email=email.lower()).username

            status = 0
            try:
                profile = Student.objects.get(user_id__username=username)
                status = 1
            except ObjectDoesNotExist:
                profile = StudentCourse.objects.get(user_id__username=username)
                status = 2
            u = profile.user_id.username

            user = authenticate(username=u,password=password)
            login(r, user)

            if status == 1:
                return redirect('student_profile')
            elif status == 2:
                return redirect('course')
            else:
                return redirect(mlogin)

    data = {"form": mu}
    return render(r, 'mlogin.html', data)




def profile(r):
    check = Student.objects.filter(user_id__username=r.user).count()
    payment = Payment.objects.filter(user_id__username=r.user)
    due = 0
    for x in payment:
        due+=x.p_due
    if check ==0:
        return render(r,'student/pending.html')
    data = {
        'std_course':StudentCourse.objects.filter(user_id__username=r.user).count(),
        'user':Student.objects.filter(user_id__username=r.user),
        'due':due
    }
    return render(r,'student/index.html',data)

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def payment(r):
    std_course = StudentCourse.objects.filter(user_id__username=r.user)
    paydata = Payment.objects.filter(user_id__username=r.user)

    for x in range(std_course.count()):
        doj = std_course[x].data_of_join
        while diff_month(datetime.now().date(), doj) != 0:
            cond = Q(p_month=doj) & Q(p_course=std_course[x].id) & Q(user_id__username=r.user)
            if Payment.objects.filter(cond).exists() == False:
                p = Payment()
                p.p_month = doj
                p.p_amount = 700
                p.p_status = "0"
                p.p_course = StudentCourse(std_course[x].id)
                p.p_due = 700
                user = User.objects.get(username=r.user)
                p.user_id = user
                p.save()
            doj = doj + datedelta(months=1)

    data = {
        'user': Student.objects.filter(user_id__username=r.user),
        "pay":paydata,
    }
    return render(r,'student/payment.html',data)


def student_course(r):
    data = {
        'course':Course.objects.exclude(studentcourse__user_id=r.user).count(),
        "stdcourse": StudentCourse.objects.filter(user_id__username=r.user),
        'user': Student.objects.filter(user_id__username=r.user),
    }
    return render(r,'student/course.html',data)


def update_payment(r,pay_id):
    a = Payment.objects.get(user_id__username=r.user,pay_id=pay_id)
    a.p_status = "1"
    a.p_due = 0
    a.save()
    return redirect('payments')

def add_course(r):
    f = AddCourseForm(r.POST or None)
    if r.method == "POST":
        if f.is_valid():
            d = f.save(commit=False)
            user = User.objects.get(username=r.user)
            d.user_id = user
            d.course_name = Course(r.POST.get('course_name'))
            d.status = "1"
            d.save()
            return redirect('student_profile')
    data = {
            'addcourse':f,
            'course':Course.objects.exclude(studentcourse__user_id=r.user),
            'user': Student.objects.filter(user_id__username=r.user)
            }
    return render(r,'student/add_course.html',data)


def full_profile(r):
    data = {
            "userdata":User.objects.filter(username=r.user),
            "user":Student.objects.filter(user_id__username=r.user)
            }
    return render(r,'student/profile.html', data)


def update_profile(r):
    id = Student.objects.get(user_id__username=r.user)
    f = UpdateProfileForm(r.POST or None,instance=id)
    data = {
        "form": f,
        "userdata": User.objects.filter(username=r.user),
        "user": Student.objects.filter(user_id__username=r.user)
    }
    if r.method == "POST":
        if f.is_valid():
            f.save()
            return redirect('full_profile')
    return render(r,'student/update_profile.html', data)


def setting(r):
    data = {}
    return render(r,'student/setting.html', data)

#admin section...............start....................
def admin_home(r):
    data = {}
    return render(r,'admin/admin_home.html',data)

def adminStudent(r):
    data = {
        'user': Student.objects.all()
    }
    return render(r,'admin/admin_student.html',data)

def adminCourse(r):
    data = {
        'course': Course.objects.all(),
        'student':StudentCourse.objects.all(),
        'courseform':CourseForm,
    }
    return render(r,'admin/admin_course.html',data)

def adminPayment(r):
    data = {
        'payment':Payment.objects.all(),
        'student':Student.objects.all()
    }
    return render(r,'admin/admin_payment.html',data)


#action function
def approvePayment(r,pay_id):
    data = Payment.objects.get(pay_id=pay_id)
    data.p_status = '2'
    data.save()
    return redirect('payment_view',std_id=r.user.username)

def declinePayment(r,pay_id):
    data = Payment.objects.get(pay_id=pay_id)
    data.p_status = '0'
    data.p_due = 700
    data.save()
    return redirect(adminPayment)

def approvestudent(r,s_id):
    data = Student.objects.get(std_id=s_id)
    if data.status == '1':
        data.status = '3'
    elif data.status == '3':
        data.status = '1'
    elif data.status == '0':
        data.status = '1'
    data.save()
    return redirect(adminStudent)


def searchstudent(r):
    if r.method == "GET":
        con = Q(first_name__icontains=r.GET.get('search')) | Q(last_name__icontains=r.GET.get('search'))
        data = {'user':Student.objects.filter(con)}
        return render(r,'admin/admin_student.html',data)

def studentPaymentView(r,std_id):
    data = {
        'payment': Payment.objects.filter(user_id__username=std_id),
    }
    return render(r,'admin/student_payment_view.html',data)

def StudentProfileView(r,std_id):
    data = {
        'student': Student.objects.get(user_id__username=std_id),
    }
    return render(r,'admin/admin_student_profile.html',data)

def StudentProfileEdit(r,s_id):
    id = Student.objects.get(std_id=s_id)
    form  = UpdateProfileForm(r.POST or None,instance=id)

    data = {
        'form':form,
    }
    return render(r,'admin/admin_student_profile.html',data)