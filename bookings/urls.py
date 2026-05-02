from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/request/', views.request_booking, name='request'),
    path('<slug:slug>/', views.detail, name='detail'),
]
