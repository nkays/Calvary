from django.urls import path 
from .views import LocationListView



app_name = 'Locations'
urlpatterns = [
    path('', LocationListView.as_view(), name='location_list')
]