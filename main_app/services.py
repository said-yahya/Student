import json
from collections import OrderedDict
from django.db import connection


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()]


def dict_fetchone(cursor):
    desc = cursor.description
    return dict(zip([col[0] for col in desc], cursor.fetchone()))


def get_student(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select s.id, s.name, s.last_name, g.branch from main_app_student s 
            left join main_app_group g on s.group_id=g.id
            where s.id = {id}
        """)
        data = dict_fetchone(cursor)
        return data


def check_student(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select * from main_app_student s
            where s.id={id}
        """)
        data = dict_fetchone(cursor)
        return data


def check_teacher(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select * from main_app_teacher t
            where t.id={id}
        """)
        data = dict_fetchone(cursor)
        return data


def get_teacher(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select t.*, s.subject_name from main_app_teacher t left join 
            main_app_subject s on t.subject_id=s.id
            where t.id={id}
        """)
        data = dict_fetchone(cursor)
        return data


def get_groups():
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select g.id, g.branch, g.class_num from main_app_group g 
            order by g.class_num;
    """)
        data = dict_fetchall(cursor)
        return data


def get_one_group(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select s.*, g.branch from main_app_student s left join main_app_group g on s.group_id=g.id
            where g.id={id}
    """)
        data = dict_fetchall(cursor)
        return data


def get_exams(teacher_id, group_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select id, exam_num, group_id from main_app_exam 
            where teacher_id={teacher_id} and group_id={group_id}
        """)
        data = dict_fetchall(cursor)
        return data


def get_exam_num(teacher_id, group_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select exam.exam_num from main_app_exam exam 
            where exam.teacher_id={teacher_id} and exam.group_id={group_id}
            order by exam.exam_num desc 
            limit 1 
        """)
        data = dict_fetchall(cursor)
        return data


def get_group_exam(group_id, exam_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
        select s.name, s.last_name, g.grade, g.exam_id, s.id from main_app_student s left join main_app_grade g on s.id=g.student_id 
        where s.group_id={group_id} and g.exam_id={exam_id} order by g.exam_id, s.id
        """)
        data = dict_fetchall(cursor)
        return data


def get_student_exams(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
        select  sub.subject_name, g.grade, e.exam_num from main_app_student s left join
         main_app_grade g on s.id=g.student_id left join main_app_exam e on g.exam_id=e.id left join 
         main_app_subject sub on e.subject_id=sub.id where s.id={id} order by sub.id
        """)
        data = dict_fetchall(cursor)
        return data


def edit_student_exam(student_id, exam_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
        select s.*, g.grade, g.id as grade_id, e.id as exam_id, e.teacher_id from main_app_student s left join main_app_grade g 
        on s.id=g.student_id left join main_app_exam e on g.exam_id=e.id where e.id={exam_id} and s.id={student_id};
        """)
        data = dict_fetchone(cursor)
        return data


def update_exam(grade, grade_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            update main_app_grade set grade={grade} where id={grade_id} 
        """)