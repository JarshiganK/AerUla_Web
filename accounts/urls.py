from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_entry, name='index'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('logout/', views.AccountLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('verification-sent/', views.verification_sent, name='verification_sent'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]
