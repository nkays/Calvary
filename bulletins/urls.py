from django.urls import path

from . import views

app_name = 'bulletins'

urlpatterns = [
    path('', views.BulletinListView.as_view(), name='list'),
    path('add/', views.BulletinCreateView.as_view(), name='add'),
    path('<int:pk>/', views.BulletinDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BulletinUpdateView.as_view(), name='update'),
    path('today/edit/', views.edit_today, name='edit_today'),
]
