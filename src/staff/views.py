# Create your views here.
from django.views.generic import ListView
from .models import StaffMember

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# @login_required
# @staff_member_required
def staff_list_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("You must log in first", status=401)
    if not user.is_staff:
        return HttpResponse("You must be staff to view this page", status=403)
    
    qs = StaffMember.objects.all()
    context = {
        "object_list": qs,
    }
    
    return render(request, "pages/list.html", context)




def staff_detail_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("You must log in first", status=401)
    if not user.is_staff:
        return HttpResponse("You must be staff to view this page", status=403)
    
    qs = StaffMember.objects.all()
    context = {
        "object": qs.first(),
    }
    return render(request, "pages/detail.html", context)



