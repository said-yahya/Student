from django.db import models

# Create your models here.


class Group(models.Model):

    branch = models.CharField(max_length=255)
    class_num = models.IntegerField()

    def __str__(self):
        return self.branch


class Subject(models.Model):

    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name


class Student(models.Model):

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Teacher(models.Model):

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Exam(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    exam_num = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Grade(models.Model):

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField()
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student