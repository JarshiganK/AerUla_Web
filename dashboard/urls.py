from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('journal/', views.cultural_journal, name='journal'),
    path(
        'passport/',
        RedirectView.as_view(permanent=False, pattern_name='dashboard:journal'),
        name='passport_legacy',
    ),
    path('vendor/', views.host_workspace, name='vendor'),
    path('vendor/experiences/new/', views.vendor_experience_create, name='vendor_experience_create'),
    path('host/', views.host_workspace, name='host'),
    path('host/experiences/new/', views.vendor_experience_create, name='host_experience_create'),
    path('admin-workspace/', views.admin_workspace, name='admin_workspace'),
]
