from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.landing_page_entry_list_view, name='entry-list'),
    path('<int:id>/', views.landing_page_entry_detail_view, name='entry-detail'),
    path('notes/', views.entry_list_notes_view, name='entry-list-notes'),
  
   
]




