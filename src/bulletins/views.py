from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Bulletin
from .forms import BulletinForm


class BulletinListView(ListView):
    model = Bulletin
    template_name = 'bulletins/bulletin_list.html'
    context_object_name = 'bulletins'
    paginate_by = 20


class BulletinDetailView(DetailView):
    model = Bulletin
    template_name = 'bulletins/bulletin_detail.html'
    context_object_name = 'bulletin'


class BulletinCreateView(CreateView):
    model = Bulletin
    form_class = BulletinForm
    template_name = 'bulletins/bulletin_form.html'
    success_url = reverse_lazy('bulletins:list')


class BulletinUpdateView(UpdateView):
    model = Bulletin
    form_class = BulletinForm
    template_name = 'bulletins/bulletin_form.html'
    success_url = reverse_lazy('bulletins:list')


# convenience shortcut for editing existing by date or redirecting to create

def edit_today(request):
    from django.utils import timezone
    today = timezone.now().date()
    bulletin, created = Bulletin.objects.get_or_create(date=today)
    return redirect('bulletins:update', pk=bulletin.pk)
