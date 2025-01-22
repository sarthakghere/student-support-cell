from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('list/', views.student_management, name='manage_students'),
    path('view/<int:pk>/', views.view_student, name='view_student'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('add/', views.add_student, name='add_student'),
    path('add/single/', views.add_single_student, name='add_single_student'),
    
]