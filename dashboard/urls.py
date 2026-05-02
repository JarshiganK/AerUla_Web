from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('passport/', views.passport, name='passport'),
    path('host/', views.host_workspace, name='host'),
    path('admin-workspace/', views.admin_workspace, name='admin_workspace'),
]
