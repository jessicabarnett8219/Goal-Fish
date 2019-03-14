from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from ..models import Student, User, GradeLevel, Goal, Evaluation
from django.urls import reverse
from django.db.models import Avg

@login_required(login_url='/login')
def weekly_progress_form(request, student_id):
    template_name = "goalfish/weekly_progress_form.html"
    current_student = get_object_or_404(Student, pk=student_id)
    available_weeks = Evaluation.objects.values('schoolWeek').filter(student=current_student).order_by('schoolWeek').distinct()
    context = {'current_student': current_student, 'available_weeks': available_weeks}

    return render(request, template_name, context)


@login_required(login_url='/login')
def weekly_progress_results(request, student_id):
    template_name = "goalfish/weekly_progress_results.html"
    current_student = get_object_or_404(Student, pk=student_id)
    school_week = request.POST["school_week"]

    evaluations = Evaluation.objects.filter(student=current_student, schoolWeek=school_week)

    score1_avg = Evaluation.objects.filter(schoolWeek=school_week, student=current_student).aggregate(Avg('score1'))
    score2_avg = Evaluation.objects.filter(schoolWeek=school_week, student=current_student).aggregate(Avg('score2'))
    score3_avg = Evaluation.objects.filter(schoolWeek=school_week, student=current_student).aggregate(Avg('score3'))
    score4_avg = Evaluation.objects.filter(schoolWeek=school_week, student=current_student).aggregate(Avg('score4'))
    score5_avg = Evaluation.objects.filter(schoolWeek=school_week, student=current_student).aggregate(Avg('score5'))
    score6_avg = Evaluation.objects.filter(schoolWeek=school_week, student=current_student).aggregate(Avg('score6'))


    return render(request, template_name, {'current_student': current_student, 'evaluations': evaluations, "school_week": school_week, 'score1_avg': score1_avg, 'score2_avg': score2_avg, 'score3_avg': score3_avg, 'score4_avg': score4_avg, 'score5_avg': score5_avg, 'score6_avg': score6_avg })