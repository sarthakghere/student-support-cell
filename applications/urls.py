from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('list/', views.list_applications, name='list_applications'),
    path('view/<int:pk>/', views.view_application, name='view_application'),
    path('print/<int:pk>/', views.print_application, name='print_application'),
]