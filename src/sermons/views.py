#src/sermons/views.py
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Sermon, Series
from django.conf import settings
from . import services

# Create your views here.
def series_list(request):
    queryset = services.get_series()
    print(queryset)
    return JsonResponse({"data": [x.id for x in queryset]})
    return render(request, 'pages/sermons/list.html', {'object_list': queryset})


def sermon_list(request):
    sermons = Sermon.objects.all()
    return render(request, 'pages/sermon_list.html', {'object_list': sermons})



def series_detail(request, series_id=None, *args, **kwargs):
    series_obj = services.get_series_detail(series_id=series_id)
    if series_obj is None:
        raise Http404("Series not found")
    return render(request, 'pages/series_detail.html', {'series': series_obj})
  


def sermon_detail(request, pk, *args, **kwargs):
    sermon_obj = services.get_sermon_detail(
        sermon_id=pk, 
        series_id=kwargs.get('series_id')
        )
    if sermon_obj is None:
        raise Http404("Sermon not found")
    sermon = get_object_or_404(Sermon, pk=pk)
    return render(request, 'pages/sermon_detail.html', {'sermon': sermon})

   
        
