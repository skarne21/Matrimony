from rest_framework import serializers
from .models import Religion, Caste, PartnerPreferences


class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = ['id', 'name']


class CasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caste
        fields = ['id', 'name', 'religion_id']


class PartnerPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerPreferences
        exclude = ['id', 'user']
