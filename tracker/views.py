from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Ad, Advertiser

class AdListView(ListView):
    model = Ad
    template_name = 'home.html'


class AddNewView(CreateView):
    model = Advertiser
    template_name = 'new.html'
    fields = '__all__'