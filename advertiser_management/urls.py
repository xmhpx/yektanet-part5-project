from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('click/<int:ad_id>/', views.click, name='click'),
    path('create_ad/', views.create_ad, name='create_ad'),
]