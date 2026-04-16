#src/sermons/views.py
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Sermon, Series
from django.conf import settings
from . import services


# Create your views here.
# def series_list(request):
#     queryset = services.get_series()
#     print(queryset)
#     # return JsonResponse({"data": [x.path for x in queryset]})
#     context = {
#         'object_list': queryset
#     }
#     return render(request, 'pages/sermons/list.html', context)

def series_detail(request, series_slug=None, *args, **kwargs):
    series_obj = services.get_series_detail(series_slug=series_slug or None or "standalone" or "default")
    if series_obj is None:
        raise Http404("Series not found")
    sermons_queryset = services.get_sermons_by_series(series_obj)
    context = {
        'object': series_obj,
        'sermons_queryset': sermons_queryset
    }
    # return JsonResponse({"data": [x.id for x in sermons_queryset]})
    return render(request, 'pages/sermons/detail.html', context)
  
# def sermon_list(request):
#     queryset = Sermon.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, 'pages/sermons/sermon_list.html', context)

def sermon_detail(request, series_slug=None, youtube_id=None, *args, **kwargs):
    print(series_slug, youtube_id)
    sermon_obj = services.get_sermon_detail(
        series_slug=series_slug, 
        youtube_id=youtube_id
        )
    context = {
        'object': sermon_obj
    }
    if sermon_obj is None:
        raise Http404("Sermon not found")
    
    return render(request, 'pages/sermons/sermon_detail.html', context)

   
        


def sermon_list(request):
    sermons = Sermon.objects.select_related("series").all()

    # --- Filters ---
    query = request.GET.get("q")
    series_id = request.GET.get("series")
    sort = request.GET.get("sort")

    if query:
        sermons = sermons.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if series_id:
        sermons = sermons.filter(series_id=series_id)

    if sort == "old":
        sermons = sermons.order_by("published_at")
    else:
        sermons = sermons.order_by("-published_at")  # default newest

    return render(request, "pages/sermons/list.html", {
        "object_list": sermons,
        "object_type": "sermon",
        "page_title": "Sermons",
        "page_subtitle": "Browse recent messages",

        # 👇 pass filter data to template
        "query": query,
        "selected_series": series_id,
        "sort": sort,
        "series_list": Series.objects.all(),
    })


def series_list(request):
    series = Series.objects.prefetch_related("sermons").all().order_by("-id")

    # --- Search only ---
    query = request.GET.get("q")

    if query:
        series = series.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, "pages/sermons/list.html", {
        "object_list": series,
        "object_type": "series",
        "page_title": "Series",
        "page_subtitle": "Browse sermon series",

        "query": query,
    })

from django.shortcuts import get_object_or_404, render

def sermon_by_series_list(request, series_slug, *args, **kwargs):

    # ✅ Get series by slug (NOT id)
    series_obj = get_object_or_404(
        Series.objects.prefetch_related("sermons"),
        slug=series_slug
    )

    # ✅ SAME logic as your working filter, just using object
    sermons_queryset = Sermon.objects.filter(
        series=series_obj
    ).select_related("series").order_by("-published_at")

    context = {
        "object": series_obj,

        "object_list": sermons_queryset,
        "object_type": "sermon",

        "page_title": series_obj.title,
        "page_subtitle": f"{sermons_queryset.count()} sermons in this series",
    }

    return render(request, "pages/sermons/list.html", context)