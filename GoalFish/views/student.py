from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from ..models import Student, User, GradeLevel, Avatar, Evaluation
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from random import *


@login_required(login_url='/login')
def list_students(request):
    '''[Queries the database for all objects in the student table that included the foreign key of the current logged in user and uses them in rendering the all_students template]

    Arguments:
        request

    Returns:
        [Rendered HTML] -- [renders the all_students template]
    '''
    current_user = request.user

    all_students = Student.objects.filter(
        user=current_user).order_by('lastName', 'firstName')
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': all_students})


def grade_filter(request):
    '''[Handles filtering students by grade level for display on the all_students.html template using posted data from the grade filter form. Queries the database looking for student's with grade level entered by the user in the form. Also filters only for student's that match the logged in user, like in the list_students view.]

    Arguments:
        request

    Returns:
        [Rendered HTML] -- [Renders the all_students.html template with the filtered students.]
    '''

    current_user = request.user
    grade = request.POST["grade"]
    students = Student.objects.filter(
        gradeLevel=grade, user=current_user).order_by('lastName', 'firstName')
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': students})


@login_required(login_url='/login')
def add_student(request):
    '''[Handles posting the data from the add_student_form.html and saves the new student to the database]

    Arguments:
        request

    Returns:
        [Redirect] -- [Redirects to the student detail page using the id of the newly saved student]
    '''

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    age = request.POST["age"]
    classroom_teacher = request.POST["classroom_teacher"]

    current_user = request.user

    grade_level_id = request.POST["grade_level"]
    grade_level = get_object_or_404(GradeLevel, pk=grade_level_id)
    random_number = random_number = randint(1, 5)
    new_avatar = get_object_or_404(Avatar, pk=random_number)

    new_student = Student(
        user=current_user,
        gradeLevel=grade_level,
        firstName=first_name,
        lastName=last_name,
        age=age,
        classroomTeacher=classroom_teacher,
        avatar=new_avatar
    )
    new_student.save()
    messages.success(request, 'The student was successfully added.')
    return HttpResponseRedirect(reverse('goalfish:student_detail', args=(new_student.id,)))


@login_required(login_url='/login')
def display_student_form(request):
    '''[Renders the add_student_form template. Queries the database for all the available grade levels in order to populate the grade level dropdown on the form]

    Arguments:
        request

    Returns:
        [Rendered HTML] -- [Renders the add student form]
    '''

    grade_levels = GradeLevel.objects.all()

    template_name = 'goalfish/add_student_form.html'

    return render(request, template_name, {'grade_levels': grade_levels})


@login_required(login_url='/login')
def student_detail(request, student_id):
    '''[Renders the student detail template. Queries the database for the student with the id specified in the URL. Only displays the student if the user foreign key matches that of the logged in user. Queries the database for any evaluations associated with that student. Only renders the 'view progress' button if the students has associated evaluations.]

    Arguments:
        request
        student_id

    Returns:
        [Rendered HTML] -- [Student detail template]
    '''

    current_user = request.user
    student = get_object_or_404(Student, pk=student_id, user=current_user)
    template_name = 'goalfish/student_detail.html'
    evaluations = Evaluation.objects.filter(student=student)

    return render(request, template_name, {"student": student, "evaluations": evaluations})


@login_required(login_url='/login')
def edit_student_form(request, student_id):
    '''[Renders the edit student form with the specific student's information pre-populated in the form. Queries the database for the student using the student id from the URL and checks to make sure the associated user matches the logged in user. Queries for all the grade levels in the database in order to populate the grade level drop down.]

    Arguments:
        request
        student_id

    Returns:
        [Rendered HTML] -- [Edit student form with student details prepopulated]
    '''

    current_user = request.user
    student = get_object_or_404(Student, pk=student_id, user=current_user)
    grade_levels = GradeLevel.objects.all()

    context = {"student": student, "grade_levels": grade_levels}
    template_name = "goalfish/edit_student_form.html"

    return render(request, template_name, context)


@login_required(login_url='/login')
def edit_student(request, student_id):
    '''[Handles posting the data from the edit student form and saving the edited student object to the database.]

    Arguments:
        request
        student_id

    Returns:
        [Redirect] -- [Redirects to the student detail page using the student id from the URL]
    '''

    student = get_object_or_404(Student, pk=student_id)

    student.firstName = request.POST["first_name"]
    student.lastName = request.POST["last_name"]
    student.age = request.POST["age"]
    student.classroomTeacher = request.POST["classroom_teacher"]

    grade_level_id = request.POST["grade_level"]
    grade_level = get_object_or_404(GradeLevel, pk=grade_level_id)
    student.gradeLevel = grade_level

    student.save()
    messages.success(request, 'Your changes were saved.')

    return HttpResponseRedirect(reverse('goalfish:student_detail', args=(student_id,)))


@login_required(login_url='/login')
def student_search(request):
    '''[Uses the data posted in the student search input from the all_students form or the navbar. Queries the database for student's whose first name or last name match the posted search.]

    Arguments:
        request

    Returns:
        [Rendered HTML] -- [Renders the all_students template with the students that match the query]
    '''

    current_user = request.user
    name_query = request.POST["name_query"]
    if ' ' in name_query:
    # Handles searches that contain a first and last name. If there is a space in the search, create a list out of the two strings. Query the database for a student whose first name matches the first list item and whose last name matches the second list item AND whose associated user is the current logged in user.
        split_name = name_query.split(" ")
        students = Student.objects.filter(Q(user=current_user), Q(
            firstName__icontains=split_name[0]), Q(lastName__icontains=split_name[1]))
    else:
    # If there's only one string in the search, query the database for students whose first name or last name match the string
        students = Student.objects.filter(Q(user=current_user), Q(
            firstName__icontains=name_query) | Q(lastName__icontains=name_query))
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': students})
