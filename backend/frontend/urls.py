from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.index),
    path('register/', views.index),
    path('home/', views.index),
]
