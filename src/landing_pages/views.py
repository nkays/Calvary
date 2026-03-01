from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import LandingPageEntry
from .forms import LandingPageEntryModelForm 


PROJECT_NAME = getattr(settings, "PROJECT_NAME", "Unset Project in Views")

def home_page(request, *args, **kwargs):
    title = "Calvary SE CT"
    form = LandingPageEntryModelForm(request.POST or None)
    
    if form.is_valid():
        obj = form.save(commit=False)
        obj.slug = obj.email
        obj.save()
        
        # print(form.cleaned_data)
        # name = form.cleaned_data.get("name")
        # email = form.cleaned_data.get("email")
        # obj = LandingPageEntry.objects.create(name=name, email=email, slug=email)
        # obj.save()
        form = LandingPageEntryModelForm()  # Reset form after successful submission
        # Form is valid - process the data
    else:
        # form.errors contains all validation errors
        print(form.errors)
    
    context = {
        "title": title,
        "form": form
    }
    parag = "Welcome {title}".format(**context)
    context["parag"] = parag
    return render(request, "pages/home.html", context)



def healthz_view(request):
    return JsonResponse({"status": "ok"})