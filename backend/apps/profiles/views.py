from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Religion, Caste
from .serializers import ReligionSerializer, CasteSerializer


class ReligionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        religions = Religion.objects.all().order_by('name')
        return Response(ReligionSerializer(religions, many=True).data)


class CasteListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        religion_id = request.query_params.get('religion_id')
        qs = Caste.objects.all().order_by('name')
        if religion_id:
            qs = qs.filter(religion_id=religion_id)
        return Response(CasteSerializer(qs, many=True).data)
