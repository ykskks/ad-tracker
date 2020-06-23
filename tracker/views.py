from django.views.generic import ListView

from .models import Ad

class AdListView(ListView):
    model = Ad
    template_name = 'home.html'