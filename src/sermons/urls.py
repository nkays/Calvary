from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.sermon_list, name='sermon_list'),
    path('series/', views.series_list, name='series_list'),
    path('<slug:series_id>/', views.series_detail, name='series_detail'),
    path('<slug:series_id>/<slug:sermon_id>/', views.sermon_detail, name='sermon_detail'),
]