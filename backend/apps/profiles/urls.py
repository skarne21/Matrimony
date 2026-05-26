from django.urls import path
from .views import ReligionListView, CasteListView

urlpatterns = [
    path('religions/', ReligionListView.as_view(), name='religions'),
    path('castes/', CasteListView.as_view(), name='castes'),
]
