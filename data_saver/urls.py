from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/data/save/', views.DataManager.as_view(), name='data_saver'),
]