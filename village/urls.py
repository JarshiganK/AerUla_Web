from django.urls import path

from . import views

app_name = 'village'

urlpatterns = [
    path('', views.placeholder, name='index'),
]
