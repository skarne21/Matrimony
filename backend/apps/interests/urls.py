from django.urls import path
from .views import (
    SendInterestView, ManageInterestView,
    ReceivedInterestsView, SentInterestsView, InterestWithUserView,
)

urlpatterns = [
    path('interests/', SendInterestView.as_view(), name='send-interest'),
    path('interests/received/', ReceivedInterestsView.as_view(), name='received-interests'),
    path('interests/sent/', SentInterestsView.as_view(), name='sent-interests'),
    path('interests/with/<uuid:user_id>/', InterestWithUserView.as_view(), name='interest-with-user'),
    path('interests/<int:pk>/', ManageInterestView.as_view(), name='manage-interest'),
]
