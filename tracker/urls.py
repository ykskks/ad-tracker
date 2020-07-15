from django.urls import path

from .views import HomeView, AdListView, AdvertiserListView, AddNewView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ad/', AdListView.as_view(), name='ad'),
    path('advertiser/', AdvertiserListView.as_view(), name='advertiser'),
    path('new/', AddNewView.as_view(), name='new')
]