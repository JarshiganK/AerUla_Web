from django.urls import path

from . import views

app_name = 'simulations'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.preview, name='preview'),
    path('<slug:slug>/quiz/', views.quiz, name='quiz'),
]
