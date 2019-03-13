from django.contrib.auth.models import User
from django.db import models


class Goal(models.Model):
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.description

class GradeLevel(models.Model):
    grade = models.CharField(max_length=1)

    def __str__(self):
        return self.grade

class Student(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    gradeLevel = models.ForeignKey(
        GradeLevel,
        on_delete=models.CASCADE,
    )
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    age = models.IntegerField()
    classroomTeacher = models.CharField(max_length=50)

    def __str__(self):
        return self.firstName, self.lastName, self.classroomTeacher

    @property
    def fullName(self):
        return self.firstName + self.lastName

class Evaluation(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    schoolWeek = models.IntegerField()
    goal1 = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal1"
    )
    score1 = models.IntegerField()
    goal2 = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal2"
    )
    score2 = models.IntegerField()
    goal3 = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal3"
    )
    score3 = models.IntegerField()
    goal4 = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal4"
    )
    score4 = models.IntegerField()
    goal5 = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal5"
    )
    score5 = models.IntegerField()
    goal6 = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal6"
    )
    score6 = models.IntegerField()
