from django.contrib import admin
from django.urls import path,include
from datawork import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', views.home,name="homepage"),
    path('contact/', views.contact,name="contact"),
    path('course/', views.course,name="course"),
    path('about/', views.about,name="about"),
    path('accounts/apply/', views.apply,name="apply"),
    path('accounts/register/', views.register,name="register"),
    path('mlogin/', views.mlogin,name="mlogin"),
    path('accounts/',include('django.contrib.auth.urls'),name="account"),
    path('student/',views.profile,name="student_profile"),
    path('student/add_course',views.add_course,name="add_course"),
    path('student/payments/',views.payment,name="payments"),
    path('student/course/',views.student_course,name="student_course"),
    path('student/update_profile/',views.update_profile,name="update_profile"),
    path('student/profile/',views.full_profile,name="full_profile"),
    path('student/setting/',views.setting,name="setting"),
    path('student/update_payments/<int:pay_id>', views.update_payment,name="update_payments"),
    path('admin/index', views.admin_home,name="admin_home"),
    path('admin/student', views.adminStudent,name="admin_student"),
    path('admin/payment', views.adminPayment,name="admin_payment"),
    path('admin/course', views.adminCourse,name="admin_course"),
    path('admin/approvepayment/<int:pay_id>', views.approvePayment,name="approve_payment"),
    path('admin/declinepayment/<int:pay_id>', views.declinePayment,name="decline_payment"),
    path('admin/approve/<int:s_id>', views.approvestudent,name="approve"),
    path('admin/searchstudent/', views.searchstudent,name="searchstudent"),
    path('admin/payment_view/<str:std_id>', views.studentPaymentView,name="payment_view"),
    path('admin/profile_view/<str:std_id>', views.StudentProfileView,name="profile_view"),
    path('admin/profile_edit/<int:s_id>', views.StudentProfileEdit,name="profile_student_edit"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

