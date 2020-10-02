from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.
class Student_custom(admin.ModelAdmin):
    def delete(self, obj):
        return format_html("<a href='/superadmin/datawork/student/{}/delete' class='deletelink'>Delete</a>".format(obj.std_id))


    def edit(self, obj):
        return format_html("<a href='/superadmin/datawork/student/{}/change' class='default'>Update</a>".format(obj.std_id))

    def pending(self, request, queryset):
        queryset.update(status='0')

    def active(self, request, queryset):
        queryset.update(status='1')

    def takeout(self, request, queryset):
        queryset.update(status='3')

    pending.short_description = "Make All Pending"
    pending.short_description = "Make All Active"
    pending.short_description = "Make All Takeout"


    action = [pending, active, takeout]


    list_display = ['first_name', 'last_name', 'father_name', 'date_of_birth', 'contact', 'gender','status']
    list_filter = ('status', )
    list_editable = ['status']
    search_fields = ('first_name', 'last_name')
    ordering = ('first_name', )

    fieldsets = (('Personal Details', {'fields': ('first_name', 'last_name', 'father_name', 'contact', 'slugs','user_id')}), ('Adress Details', {'fields':('address',),}))


prepopulated_fields = {'slugs': ['first_name']}

admin.site.site_header = "CWS Panel"

class Payment_custom(admin.ModelAdmin):
    list_display = ['user_id', 'p_month', 'p_amount']
    search_fields = ('user_id', 'p_month')


class Course_custom(admin.ModelAdmin):
    list_display = ['course_name', 'course_duration', 'course_fees']
    search_fields = ('course_name', 'course_duration')


admin.site.register(Student, Student_custom)
admin.site.register(Payment, Payment_custom)
admin.site.register(Course, Course_custom)
admin.site.register(StudentCourse)


