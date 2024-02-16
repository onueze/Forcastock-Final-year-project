from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.loginPage),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('verify_code_register/', views.verify_code_register, name='verify_code_register'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
]

