#src/sermons/views.py
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sermon, Series
from django.conf import settings
from . import services

# Create your views here.
def series_list(request):
    queryset = services.get_series()
    print(queryset)
    # return JsonResponse({"data": [x.path for x in queryset]})
    context = {
        'object_list': queryset
    }
    return render(request, 'pages/sermons/list.html', context)

def series_detail(request, series_id=None, *args, **kwargs):
    series_obj = services.get_series_detail(series_id=series_id)
    if series_obj is None:
        raise Http404("Series not found")
    sermons_queryset = services.get_sermons_by_series(series_obj)
    context = {
        'object': series_obj,
        'sermons_queryset': sermons_queryset
    }
    # return JsonResponse({"data": [x.id for x in sermons_queryset]})
    return render(request, 'pages/sermons/detail.html', context)
  
def sermon_list(request):
    queryset = Sermon.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'pages/sermon_list.html', context)

def sermon_detail(request, series_id=None, sermon_id=None, *args, **kwargs):
    print(series_id, sermon_id)
    sermon_obj = services.get_sermon_detail(
        series_id=series_id, 
        sermon_id=sermon_id
        )
    context = {
        'object': sermon_obj
    }
    if sermon_obj is None:
        raise Http404("Sermon not found")
    
    return render(request, 'pages/sermon_detail.html', context)

   
        
