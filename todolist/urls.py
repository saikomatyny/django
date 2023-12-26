from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('getToDoList/', views.getToDoList),
    path('postToDoList/', views.postToDoList),
    path('deleteToDoList/', views.deleteToDoList),
]
