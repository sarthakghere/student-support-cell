from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/list/', views.staff_management, name='manage_staff'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('view/<int:pk>/', views.view_staff, name='view_staff'),
    path('edit/<int:pk>/', views.edit_staff, name='edit_staff'),
    path('delete/<int:pk>/', views.delete_staff, name='delete_staff'),

]