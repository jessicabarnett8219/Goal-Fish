from django.conf.urls import url
from django.urls import path

from . import views

app_name = "goalfish"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    path('students/', views.list_students, name='all_students'),
    path('add-student/', views.display_student_form, name='add_student_form'),
    path('student-added/', views.add_student, name='add_student'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('new-evaluation/<int:student_id>/', views.display_eval_form, name='new_eval'),
]
