"""
URL configuration for student_support_cell project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('students/', include('students.urls')),
    path('', lambda request: redirect('authentication:admin_dashboard') if request.user.is_authenticated and request.user.role == 'admin' else redirect('authentication:staff_dashboard') if request.user.is_authenticated and request.user.role == 'staff' else redirect('authentication:login'), name='home'),
    path('certificates/', include('certificates.urls')),
    path('applications/', include('applications.urls')),
]
