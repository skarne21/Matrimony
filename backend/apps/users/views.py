import random
import logging

from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

OTP_TTL = 600  # 10 minutes


def _generate_otp():
    return str(random.randint(100000, 999999))


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Registration successful. Please verify your phone number.'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number', '').strip()
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'No account found with this phone number.'}, status=status.HTTP_404_NOT_FOUND)

        otp = _generate_otp()
        cache.set(f'otp_{phone_number}', otp, timeout=OTP_TTL)

        # Dev: OTP printed to Django console. Replace with MSG91 call in production.
        print(f'\n[DEV OTP] {phone_number} → {otp}\n')
        logger.info('OTP generated for %s', phone_number)

        return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number', '').strip()
        otp = request.data.get('otp', '').strip()

        if not phone_number or not otp:
            return Response({'error': 'Phone number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(f'otp_{phone_number}')
        if not cached_otp or cached_otp != otp:
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        cache.delete(f'otp_{phone_number}')

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': str(user.id),
        }, status=status.HTTP_200_OK)
