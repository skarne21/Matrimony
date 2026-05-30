from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class InboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        me = request.user

        # Backfill: create conversations for accepted interests that don't have one yet
        from apps.interests.models import Interest, InterestStatus
        orphans = Interest.objects.filter(
            status=InterestStatus.ACCEPTED
        ).filter(
            Q(sender=me) | Q(receiver=me)
        ).filter(conversation__isnull=True)
        for interest in orphans:
            Conversation.objects.get_or_create(
                interest=interest,
                defaults={'user_one': interest.sender, 'user_two': interest.receiver},
            )

        convs = (
            Conversation.objects
            .filter(user_one=me) | Conversation.objects.filter(user_two=me)
        ).order_by('-last_message_at')
        return Response(ConversationSerializer(convs, many=True, context={'request': request}).data)


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        conv = get_object_or_404(Conversation, id=conversation_id)
        if request.user not in (conv.user_one, conv.user_two):
            return Response(status=status.HTTP_403_FORBIDDEN)

        conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

        msgs = conv.messages.order_by('created_at')
        return Response(MessageSerializer(msgs, many=True).data)

    def post(self, request, conversation_id):
        conv = get_object_or_404(Conversation, id=conversation_id)
        if request.user not in (conv.user_one, conv.user_two):
            return Response(status=status.HTTP_403_FORBIDDEN)

        text = request.data.get('content_text', '').strip()
        if not text:
            return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(conversation=conv, sender=request.user, content_text=text)
        conv.last_message_at = timezone.now()
        conv.save(update_fields=['last_message_at'])

        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)
