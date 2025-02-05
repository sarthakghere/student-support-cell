from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificates, name='certificates_home'),
    path('bonafide-certificate/', views.bonafide_certificate, name='bonafide_certificate'),
    path('download-certificate/<int:certificate_id>/', views.download_certificate, name='download_certificate'),
    path('approved-duplicate-certificate/', views.approved_duplicate_certificate, name='approved_duplicate_certificate'),

]