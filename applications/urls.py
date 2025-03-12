from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('list/', views.list_applications, name='list_applications'),
]