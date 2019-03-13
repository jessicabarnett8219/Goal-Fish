from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from ..models import Student, User, GradeLevel
from django.urls import reverse
from django.db.models import Q



@login_required(login_url='/login')
def list_students(request):
    '''[Queries the database for all objects in the student table and uses them in rendering the all_students template]

    Arguments:
        request

    Returns:
        [render] -- [renders the all_students template]
    '''
    current_user = request.user

    all_students = Student.objects.filter(user=current_user)
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': all_students})

def grade_filter(request):
    current_user = request.user
    grade = request.POST["grade"]
    students = Student.objects.filter(gradeLevel=grade, user=current_user)
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': students})

@login_required(login_url='/login')
def add_student(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    age = request.POST["age"]
    classroom_teacher = request.POST["classroom_teacher"]

    current_user = request.user

    grade_level_id = request.POST["grade_level"]
    grade_level = get_object_or_404(GradeLevel, pk=grade_level_id)

    new_student = Student(
        user = current_user,
        gradeLevel = grade_level,
        firstName = first_name,
        lastName = last_name,
        age = age,
        classroomTeacher = classroom_teacher
    )
    new_student.save()
    return HttpResponseRedirect(reverse('goalfish:student_detail', args=(new_student.id,)))



@login_required(login_url='/login')
def display_student_form(request):
    grade_levels = GradeLevel.objects.all()

    template_name = 'goalfish/add_student_form.html'

    return render(request, template_name, {'grade_levels': grade_levels})

@login_required(login_url='/login')
def student_detail(request, student_id):
    current_user = request.user
    student = get_object_or_404(Student, pk=student_id, user=current_user)
    template_name = 'goalfish/student_detail.html'

    return render(request, template_name, {"student": student})

@login_required(login_url='/login')
def edit_student_form(request, student_id):
    current_user = request.user
    student = get_object_or_404(Student, pk=student_id, user=current_user)
    grade_levels = GradeLevel.objects.all()

    context = {"student": student, "grade_levels": grade_levels}
    template_name = "goalfish/edit_student_form.html"

    return render(request, template_name, context)

@login_required(login_url='/login')
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)


    student.firstName = request.POST["first_name"]
    student.lastName = request.POST["last_name"]
    student.age = request.POST["age"]
    student.classroomTeacher = request.POST["classroom_teacher"]

    grade_level_id = request.POST["grade_level"]
    grade_level = get_object_or_404(GradeLevel, pk=grade_level_id)
    student.gradeLevel = grade_level

    student.save()
    return HttpResponseRedirect(reverse('goalfish:student_detail', args=(student_id,)))

@login_required(login_url='/login')
def student_search(request):
    current_user = request.user
    name_query = request.POST["name_query"]
    students = Student.objects.filter(Q(user=current_user), Q(firstName__icontains=name_query) | Q(lastName__icontains=name_query))
    template_name = 'goalfish/all_students.html'
    return render(request, template_name, {'students': students})










