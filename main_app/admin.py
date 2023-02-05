from django.contrib import admin

# Register your models here.
from .models import Student, Teacher, Group, Subject, Exam, Grade


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(Grade)