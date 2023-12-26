from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('getToDoList/', views.get_endpoint),
    path('postToDoList/', views.post_endpoint),
    path('deleteToDoList/', views.delete_endpoint),
]
