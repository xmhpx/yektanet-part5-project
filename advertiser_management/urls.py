from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('click/<int:ad_id>/', click, name='click'),
    path('create_ad/', CreateAdView.as_view(), name='create_ad'),
    path('create_ad2/', CreateAdView2.as_view(), name='create_ad2'),
    path('detail/', DetailView.as_view(), name='detail_view'),
]