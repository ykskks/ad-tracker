from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from .models import Ad, Advertiser


class HomeView(TemplateView):
    template_name = 'home.html'


class AdListView(ListView):
    model = Ad
    template_name = 'ad.html'


class AdvertiserListView(ListView):
    model = Advertiser
    template_name = 'advertiser.html'


class AddNewView(CreateView):
    model = Advertiser
    template_name = 'new.html'
    fields = '__all__'