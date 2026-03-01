from django.urls import path ,include
from . import views



app_name = 'staff'
urlpatterns = [
    path('', views.staff_list_view, name='entry-list'),
    path('<int:id>/', views.staff_detail_view, name='entry-detail'),  
]