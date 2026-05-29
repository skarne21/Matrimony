from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Interest, InterestStatus
from .serializers import InterestSerializer

User = get_user_model()


class SendInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver_id')
        if not receiver_id:
            return Response({'error': 'receiver_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.id) == str(receiver_id):
            return Response({'error': 'You cannot send interest to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        receiver = get_object_or_404(User, id=receiver_id)

        existing = Interest.objects.filter(sender=request.user, receiver=receiver).first()
        if existing:
            if existing.status == InterestStatus.WITHDRAWN:
                existing.status = InterestStatus.PENDING
                existing.save()
                return Response(InterestSerializer(existing).data)
            return Response(
                {'error': 'Interest already exists.', 'interest': InterestSerializer(existing).data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        interest = Interest.objects.create(sender=request.user, receiver=receiver)
        return Response(InterestSerializer(interest).data, status=status.HTTP_201_CREATED)


class ManageInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        interest = get_object_or_404(Interest, id=pk)
        action = request.data.get('action')

        if action == 'withdraw':
            if interest.sender != request.user:
                return Response({'error': 'Only the sender can withdraw.'}, status=status.HTTP_403_FORBIDDEN)
            interest.status = InterestStatus.WITHDRAWN

        elif action == 'accept':
            if interest.receiver != request.user:
                return Response({'error': 'Only the receiver can accept.'}, status=status.HTTP_403_FORBIDDEN)
            if interest.status != InterestStatus.PENDING:
                return Response({'error': 'Interest is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
            interest.status = InterestStatus.ACCEPTED

        elif action == 'decline':
            if interest.receiver != request.user:
                return Response({'error': 'Only the receiver can decline.'}, status=status.HTTP_403_FORBIDDEN)
            if interest.status != InterestStatus.PENDING:
                return Response({'error': 'Interest is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
            interest.status = InterestStatus.DECLINED

        else:
            return Response({'error': 'action must be accept, decline, or withdraw.'}, status=status.HTTP_400_BAD_REQUEST)

        interest.save()
        return Response(InterestSerializer(interest).data)


class ReceivedInterestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interests = (
            Interest.objects
            .filter(receiver=request.user, status=InterestStatus.PENDING)
            .select_related('sender__profile')
            .order_by('-created_at')
        )
        return Response(InterestSerializer(interests, many=True).data)


class SentInterestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interests = (
            Interest.objects
            .filter(sender=request.user)
            .exclude(status=InterestStatus.WITHDRAWN)
            .select_related('receiver__profile')
            .order_by('-created_at')
        )
        return Response(InterestSerializer(interests, many=True).data)


class InterestWithUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        sent = Interest.objects.filter(sender=request.user, receiver__id=user_id).first()
        if sent:
            return Response({'id': sent.id, 'status': sent.status, 'direction': 'sent'})

        received = Interest.objects.filter(sender__id=user_id, receiver=request.user).first()
        if received:
            return Response({'id': received.id, 'status': received.status, 'direction': 'received'})

        return Response(None)
