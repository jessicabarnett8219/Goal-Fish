from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from ..models import Student, User, GradeLevel, Goal, Evaluation
from django.urls import reverse
from django.db.models import Avg


@login_required(login_url='/login')
def progress_form(request, student_id):
    '''[Renders the form that allows users to select which week they want to view a students scores and averages for. Queries the database for all evaluations associated with the student and only renders weeks as options that that students has an evaluating associated with. ]

    Arguments:
        request
        student_id

    Returns:
        [Rendered HTML] -- [The weekly_progress_form.html template with the weeks dropdown populated with weeks that the student has evaluations for. ]
    '''

    template_name = "goalfish/progress_landing.html"
    current_student = get_object_or_404(Student, pk=student_id)
    available_weeks = Evaluation.objects.values('schoolWeek').filter(
        student=current_student).order_by('schoolWeek').distinct()
    context = {'current_student': current_student,
               'available_weeks': available_weeks}

    return render(request, template_name, context)


@login_required(login_url='/login')
def weekly_progress_results(request, student_id):
    '''[Handles posting the data from the weekly progress form and rendering HTML with the scores for each goal for each day of that week that has an associated evaluation and the average score for that week.]

    Arguments:
            request
            student_id

    Returns:
        [Rendered HTML] -- [weekly_progress.html template with that week's scores and average for each goal.]
    '''
    template_name = "goalfish/weekly_progress_results.html"
    current_student = get_object_or_404(Student, pk=student_id)
    # Gets the school week from the weekly_progress_form input
    school_week = request.POST["school_week"]
    # Querying the database for the weeks needed to populate the weekly_progress form, which is rendered on the results page so that the user can select another week to view from that page.
    available_weeks = Evaluation.objects.values('schoolWeek').filter(
        student=current_student).order_by('schoolWeek').distinct()

    # Queries the database for any evaluations associated with that student and that school week.
    evaluations = Evaluation.objects.filter(
        student=current_student, schoolWeek=school_week)

    # Calculates the average score for all the scores associated with that goal and week and passes them as context so that they can be rendered in the progress results.
    score1_avg = Evaluation.objects.filter(
        schoolWeek=school_week, student=current_student).aggregate(Avg('score1'))
    score2_avg = Evaluation.objects.filter(
        schoolWeek=school_week, student=current_student).aggregate(Avg('score2'))
    score3_avg = Evaluation.objects.filter(
        schoolWeek=school_week, student=current_student).aggregate(Avg('score3'))
    score4_avg = Evaluation.objects.filter(
        schoolWeek=school_week, student=current_student).aggregate(Avg('score4'))
    score5_avg = Evaluation.objects.filter(
        schoolWeek=school_week, student=current_student).aggregate(Avg('score5'))
    score6_avg = Evaluation.objects.filter(
        schoolWeek=school_week, student=current_student).aggregate(Avg('score6'))

    context = {'current_student': current_student, 'evaluations': evaluations, "school_week": school_week, 'score1_avg': score1_avg, 'score2_avg': score2_avg,
               'score3_avg': score3_avg, 'score4_avg': score4_avg, 'score5_avg': score5_avg, 'score6_avg': score6_avg, 'available_weeks': available_weeks}

    return render(request, template_name, context)

@login_required(login_url='/login')
def range_progress_results(request, student_id):

    current_student = get_object_or_404(Student, pk=student_id)

    start_week = request.POST["start_week"]
    end_week = request.POST["end_week"]

    start_week = int(start_week)
    end_week = int(end_week)+1

    available_weeks = Evaluation.objects.values('schoolWeek').filter(
        student=current_student).order_by('schoolWeek').distinct()

    week_range = list(range(start_week, end_week))

    evaluations = Evaluation.objects.filter(student=current_student)
    evaluations = evaluations.filter(schoolWeek__gte=start_week)
    evaluations = evaluations.filter(schoolWeek__lte=end_week)

    score1_averages = []
    score2_averages = []
    score3_averages = []
    score4_averages = []
    score5_averages = []
    score6_averages = []

    for week in week_range:
        score1_averages.append(Evaluation.objects.filter(schoolWeek=week, student=current_student).aggregate(Avg('score1')))
        score2_averages.append(Evaluation.objects.filter(schoolWeek=week, student=current_student).aggregate(Avg('score2')))
        score3_averages.append(Evaluation.objects.filter(schoolWeek=week, student=current_student).aggregate(Avg('score3')))
        score4_averages.append(Evaluation.objects.filter(schoolWeek=week, student=current_student).aggregate(Avg('score4')))
        score5_averages.append(Evaluation.objects.filter(schoolWeek=week, student=current_student).aggregate(Avg('score5')))
        score6_averages.append(Evaluation.objects.filter(schoolWeek=week, student=current_student).aggregate(Avg('score6')))

    context = {'evaluations': evaluations, 'current_student': current_student, 'available_weeks': available_weeks, 'week_range': week_range, 'score1_averages': score1_averages }



    return render(request, "goalfish/range_progress_results.html", context)



