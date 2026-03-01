from django.shortcuts import render


# Create your views here.
# locations/views.py
from django.views.generic import ListView
from .models import Location


class LocationListView(ListView):
    model = Location
    template_name = 'pages/location_list.html'  # we'll create this next
    context_object_name = 'locations'               # nicer than default 'object_list'
    ordering = ['order', 'title']                   # match your model's Meta ordering
    
    # Optional: only show visible top-level items (or all — your call)
    # def get_queryset(self):
    #     return Location.objects.filter(is_visible=True, parent=None)