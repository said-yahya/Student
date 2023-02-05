from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('student/<int:id>/', student_info, name='student_info'),
    path('teacher/<int:id>/', teacher_info, name='teacher_info'),
    path('groups/', groups, name='groups'),
    path('group/detail/<int:id>/', group_detail, name='group_detail'),
    path('old-exams/<int:teacher_id>/<int:group_id>', old_exams, name='old_exams'),
    path('new-exam/<int:teacher_id>/<int:group_id>/', new_exam, name='new_exam'),
    path('group-exam/<int:teacher_id>/<int:group_id>/<int:exam_id>', group_exam, name='group_exam'),
    path('edit-exam/<int:exam_id>/<int:student_id>', edit_exam, name='edit_exam'),
]