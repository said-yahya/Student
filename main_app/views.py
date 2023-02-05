from django.shortcuts import render, redirect, HttpResponse
from .services import get_student, check_student, check_teacher, get_teacher, get_groups, get_one_group,\
                    get_exams, get_exam_num, get_group_exam, get_student_exams, edit_student_exam, update_exam
from .models import *
# Create your views here.


def index(request):
    if request.POST:
        data = request.POST
        if data.get('std_name'):
            check = check_student(int(data.get('std_id')))
            if check:
                if (check.get('name') == data.get('std_name')) and (check.get('last_name') == data.get('std_lastname')):
                    return redirect(f"student/{int(data.get('std_id'))}/")
        elif data.get('teach_name'):
            check = check_teacher(int(data.get('teach_id')))
            if check:
                if (check.get('name') == data.get('teach_name')) and \
                        (check.get('last_name') == data.get('teach_lastname')):
                    return redirect(f"teacher/{int(data.get('teach_id'))}/")
    return render(request, 'index.html', {})


def student_info(request, id):
    std = get_student(id)
    exams = get_student_exams(id)
    exam_list = []
    for i in range(0, len(exams)):
        subject = exams[i].get('subject_name')
        if len(exam_list) == 0:
            subject = exams[i].get('subject_name')
            exam_list.append({'subject_name': subject, 'grades': [exams[i].get('grade')]})
        elif subject == exam_list[-1].get('subject_name'):
            exam_list[-1]['grades'].append(exams[i].get('grade'))
        else:
            subject = exams[i].get('subject_name')
            exam_list.append({'subject_name': subject, 'grades': [exams[i].get('grade')]})
    average = []
    for j in exam_list:
        sub = j.get('subject_name')
        grade = sum(j.get('grades')) / len(j.get('grades'))
        average.append({'subject': sub, 'average': grade})
    context = {
        'std': std,
        'exams': exam_list,
        'averages': average
    }
    return render(request, 'student_info.html', context)


def teacher_info(request, id):
    teach = get_teacher(id)
    group = get_groups()
    context = {
        'teacher': teach,
        'groups': group
    }
    return render(request, 'teacher.html', context)


def groups(request):
    group = get_groups()
    context = {
        'groups': group
    }
    return render(request, 'classes.html', context)


def group_detail(request, id):
    group = get_one_group(id)
    context = {
        'students': group
    }
    return render(request, 'group_detail.html', context)


def old_exams(request, teacher_id, group_id):
    exams = get_exams(teacher_id, group_id)
    teacher = get_teacher(teacher_id)
    context = {
        'exams': exams,
        'teacher': teacher
    }
    return render(request, 'old_exams.html', context)


def new_exam(request, group_id, teacher_id):

    group = get_one_group(group_id)
    teacher = get_teacher(teacher_id)
    list_student_id = []
    if request.POST:
        for i in group:
            list_student_id.append(i.get('id'))
        data = request.POST
        number = get_exam_num(teacher_id, group_id)
        if data.getlist('grade'):

            exam_num = 1
            subject = Subject.objects.get(id=teacher['subject_id'])
            teach = Teacher.objects.get(id=teacher_id)
            group = Group.objects.get(id=group_id)
            if number:

                exam_num = number[0]['exam_num'] + 1
            exam, create = Exam.objects.get_or_create(
                subject=subject,
                teacher=teach,
                group=group,
                exam_num=exam_num
                )
            list_grade = data.getlist('grade')
            for i in range(len(list_student_id)):
                grade, create = Grade.objects.get_or_create(
                    exam=exam,
                    student_id=list_student_id[i],
                    grade=int(list_grade[i]))
            return redirect(f'http://127.0.0.1:8000/teacher/{teacher_id}/')
    context = {
        'group': group,
        'teacher': teacher
    }
    return render(request, 'new_exam.html', context)


def group_exam(request, teacher_id, group_id, exam_id):
    exams = get_group_exam(group_id, exam_id)
    context = {
        'teacher_id': teacher_id,
        'group_id': group_id,
        'exams': exams
    }
    return render(request, 'group_exam.html', context)


def edit_exam(request, exam_id, student_id):
    student = edit_student_exam(student_id, exam_id)
    if request.POST:
        data = request.POST
        update_exam(data.get('grade'), student.get('grade_id'))
        return redirect(f"http://127.0.0.1:8000/group-exam/"
                        f"{student.get('teacher_id')}/{student.get('group_id')}/{exam_id}")
    context = {
        'student': student
    }
    return render(request, 'edit_exam.html', context)
