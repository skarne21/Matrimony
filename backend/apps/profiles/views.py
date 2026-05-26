from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Religion, Caste, Profile
from .serializers import (
    ReligionSerializer, CasteSerializer,
    ProfileCardSerializer, ProfileDetailSerializer,
)

PAGE_SIZE = 20


class ReligionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(ReligionSerializer(Religion.objects.all().order_by('name'), many=True).data)


class CasteListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Caste.objects.all().order_by('name')
        religion_id = request.query_params.get('religion_id')
        if religion_id:
            qs = qs.filter(religion_id=religion_id)
        return Response(CasteSerializer(qs, many=True).data)


class MatchFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            my_profile = user.profile
            prefs = user.partner_preferences
        except Exception:
            return Response({'results': [], 'page': 1, 'total': 0, 'has_next': False})

        gender_map = {'male': 'female', 'female': 'male'}
        target_gender = gender_map.get(my_profile.gender)

        qs = Profile.objects.exclude(user=user).select_related('religion', 'user')
        if target_gender:
            qs = qs.filter(gender=target_gender)

        today = date.today()
        try:
            max_dob = today.replace(year=today.year - prefs.age_min)
        except ValueError:
            max_dob = today.replace(year=today.year - prefs.age_min, day=28)
        try:
            min_dob = today.replace(year=today.year - prefs.age_max)
        except ValueError:
            min_dob = today.replace(year=today.year - prefs.age_max, day=28)
        qs = qs.filter(dob__gte=min_dob, dob__lte=max_dob)

        if prefs.acceptable_religions:
            qs = qs.filter(religion_id__in=prefs.acceptable_religions)

        page = max(1, int(request.query_params.get('page', 1)))
        offset = (page - 1) * PAGE_SIZE
        total = qs.count()
        profiles = qs.order_by('-created_at')[offset:offset + PAGE_SIZE]

        return Response({
            'results': ProfileCardSerializer(profiles, many=True).data,
            'page': page,
            'total': total,
            'has_next': offset + PAGE_SIZE < total,
        })


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(
            Profile.objects.select_related('religion', 'caste'),
            user__id=pk,
        )
        return Response(ProfileDetailSerializer(profile).data)
