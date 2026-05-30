from django.urls import path
from .views import InboxView, MessageListView

urlpatterns = [
    path('conversations/', InboxView.as_view()),
    path('conversations/<uuid:conversation_id>/messages/', MessageListView.as_view()),
]
