from django.urls import path
from .views import ReligionListView, CasteListView, MatchFeedView, ProfileDetailView

urlpatterns = [
    path('religions/', ReligionListView.as_view(), name='religions'),
    path('castes/', CasteListView.as_view(), name='castes'),
    path('matches/', MatchFeedView.as_view(), name='matches'),
    path('users/<uuid:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]
