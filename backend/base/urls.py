from django.urls import path
from . import views

urlpatterns = [
    #path('', views.loginPage),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('verify_code_register/', views.verify_code_register, name='verify_code_register'),
]

