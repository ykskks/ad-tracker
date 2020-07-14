from django.urls import path

from .views import AdListView, AddNewView

urlpatterns = [
    path('', AdListView.as_view(), name='home'),
    path('new/', AddNewView.as_view(), name='new')
]