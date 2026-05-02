from django.urls import path

from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('<slug:slug>/', views.detail, name='detail'),
]
