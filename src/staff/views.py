from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import StaffMember

class StaffListView(ListView):
    model = StaffMember
    template_name = 'pages/staff_list.html'
    context_object_name = 'staff_members'

    def get_queryset(self):
        return StaffMember.objects.filter(is_visible=True).select_related('location')