from django.urls import path 
from .views import StaffListView



app_name = 'staff'
urlpatterns = [
    path('', StaffListView.as_view(), name='staff_list')
]