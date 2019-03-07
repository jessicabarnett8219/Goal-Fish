from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from ..models import Student, User, GradeLevel
from django.urls import reverse


@login_required
def list_students(request):
    '''[Queries the database for all objects in the student table and uses them in rendering the all_students template]

    Arguments:
        request

    Returns:
        [render] -- [renders the all_students template]
    '''

    all_students = Student.objects.all()
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': all_students})

@login_required
def add_student(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    age = request.POST["age"]
    classroom_teacher = request.POST["classroom_teacher"]

    current_user_id = request.user.id
    user = get_object_or_404(User, pk=current_user_id)
    grade_level = get_object_or_404(GradeLevel, pk=1)

    new_student = Student(
        user = user,
        gradeLevel = grade_level,
        firstName = first_name,
        lastName = last_name,
        age = age,
        classroomTeacher = classroom_teacher
    )
    new_student.save()
    return HttpResponseRedirect(reverse('goalfish:all_students'))

@login_required
def display_student_form(request):

    template_name = 'goalfish/add_student_form.html'

    return render(request, template_name)
