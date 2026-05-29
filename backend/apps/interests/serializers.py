from datetime import date
from rest_framework import serializers
from .models import Interest
from apps.profiles.models import Profile


def _calc_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class InterestProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name', 'age', 'city', 'state', 'occupation', 'profile_pic_url', 'is_verified']

    def get_age(self, obj):
        return _calc_age(obj.dob)


class InterestSerializer(serializers.ModelSerializer):
    sender_profile = InterestProfileSerializer(source='sender.profile', read_only=True)
    receiver_profile = InterestProfileSerializer(source='receiver.profile', read_only=True)

    class Meta:
        model = Interest
        fields = ['id', 'status', 'created_at', 'sender_profile', 'receiver_profile']
