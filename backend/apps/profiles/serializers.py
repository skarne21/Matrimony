from datetime import date
from rest_framework import serializers
from .models import Religion, Caste, PartnerPreferences, Profile


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


def _calc_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class ProfileCardSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    age = serializers.SerializerMethodField()
    religion_name = serializers.CharField(source='religion.name', default='', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user_id', 'first_name', 'last_name', 'age',
            'city', 'state', 'occupation', 'religion_name',
            'profile_pic_url', 'is_verified',
        ]

    def get_age(self, obj):
        return _calc_age(obj.dob)


class ProfileDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    age = serializers.SerializerMethodField()
    religion_name = serializers.CharField(source='religion.name', default='', read_only=True)
    caste_display = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'user_id', 'first_name', 'last_name', 'age', 'gender',
            'marital_status', 'height_cm', 'weight_kg', 'profile_created_by',
            'mother_tongue', 'religion_name', 'caste_name', 'caste_display',
            'sub_caste', 'nakshatra', 'rashi', 'is_manglik',
            'education_level', 'college', 'occupation', 'company',
            'annual_income', 'work_location',
            'father_name', 'father_occupation', 'mother_name', 'mother_occupation',
            'brothers_count', 'sisters_count', 'family_type', 'family_status',
            'eating_habit', 'smoking_habit', 'drinking_habit', 'hobbies',
            'bio', 'photo_privacy', 'profile_pic_url', 'is_verified',
            'city', 'state', 'country', 'postal_code',
        ]

    def get_age(self, obj):
        return _calc_age(obj.dob)

    def get_caste_display(self, obj):
        if obj.caste_name:
            return obj.caste_name
        return obj.caste.name if obj.caste else ''
