from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.sermon_list, name='sermon_list'),
    path('series/', views.series_list, name='series_list'),
    path('<slug:series_slug>/', views.sermon_by_series_list, name='sermon_by_series_list'),
    path('<slug:series_slug>/<slug:youtube_id>/', views.sermon_detail, name='sermon_detail'),
]