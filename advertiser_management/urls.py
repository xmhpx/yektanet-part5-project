from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inc_clicks/', views.inc_clicks, name='inc_clicks'),
    path('create_ad/', views.create_ad, name='create_ad'),
]