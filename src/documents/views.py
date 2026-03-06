from django.shortcuts import render
from django.shortcuts import render
from .models import Document
from django.conf import settings


# Create your views here.
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/list.html', {'documents': documents})

def document_detail(request, pk):
    document = Document.objects.get(pk=pk)
    return render(request, 'documents/detail.html', {'document': document})

   
        
def document_accordian(request, *args, **kwargs):

    
    doc = Document.objects.all()
    
    # or if you prefer being very explicit:
    # qs = StaffMember.objects.filter(is_visible=True).order_by('order', 'name')
    
    context = {
        "doc_list": doc,        
    }
    
    return render(request, "pages/accordian.html", context)