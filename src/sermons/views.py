#src/sermons/views.py
from django.shortcuts import render, get_object_or_404
from .models import Sermon
from django.conf import settings


# Create your views here.
def sermon_list(request):
    sermons = Sermon.objects.all()
    return render(request, 'pages/sermon_list.html', {'object_list': sermons})

def sermon_detail(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    return render(request, 'pages/sermon_detail.html', {'sermon': sermon})

   
        
