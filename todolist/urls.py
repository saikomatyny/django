from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get_endpoint/', views.get_endpoint),
    path('post_endpoint/', views.post_endpoint)
]
