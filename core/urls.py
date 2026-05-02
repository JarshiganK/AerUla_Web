from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('guide/', views.guide, name='guide'),
    path('guide/chat/', views.guide_chat_api, name='guide_chat_api'),
]
