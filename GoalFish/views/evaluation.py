from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from ..models import Student, User, GradeLevel, Goal
from django.urls import reverse

@login_required
def display_eval_form(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    goals = Goal.objects.all()

    template_name = "goalfish/eval_form.html"

    return render(request, template_name, {'student': student, 'goals': goals})

# @login_required
# def new_evaluation(request, student_id):
#     student = get_object_or_404(Student, pk=student_id)

#     return render(request, template_name, {'student': student, 'goals': goals})

# @login_required
# def edit_evaluation(request, student_id):

# @login_required
# def delete_evaluation(request, student_id):

