from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.applications_home, name='applications_home'),
    path('list/', views.list_applications, name='list_applications'),
    path('archived/', views.list_archived_applications, name='list_archived_applications'),
    path('archive/<int:pk>/', views.archive_application, name='archive_application'),
    path('unarchive/<int:pk>/', views.unarchive_application, name='unarchive_application'),
    
    path('view/<int:pk>/', views.view_application, name='view_application'),
    path('print/<int:pk>/', views.print_application, name='print_application'),
]