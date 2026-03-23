from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.sermon_list, name='sermon_list'),
    path('series/', views.series_list, name='series_list'),
    path('sermons/<int:pk>/', views.sermon_detail, name='sermon_detail'),
    path('series/<int:pk>/', views.series_detail, name='series_detail'),
    
]