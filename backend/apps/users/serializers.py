from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.profiles.models import Profile, PartnerPreferences, Religion, Caste
from apps.profiles.serializers import PartnerPreferencesSerializer

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    # --- Contact / auth ---
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    # --- Step 1: Basic ---
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'])
    dob = serializers.DateField()
    marital_status = serializers.ChoiceField(choices=['never_married', 'divorced', 'widowed'])
    height_cm = serializers.IntegerField(required=False, allow_null=True)
    weight_kg = serializers.IntegerField(required=False, allow_null=True)
    profile_created_by = serializers.ChoiceField(
        choices=['self', 'parent', 'relative', 'friend'],
        default='self',
    )

    # --- Step 2: Personal & Religion ---
    mother_tongue = serializers.CharField(required=False, allow_blank=True, default='')
    religion_id = serializers.IntegerField(required=False, allow_null=True)
    caste_id = serializers.IntegerField(required=False, allow_null=True)
    caste_name = serializers.CharField(required=False, allow_blank=True, default='')
    sub_caste = serializers.CharField(required=False, allow_blank=True, default='')
    nakshatra = serializers.CharField(required=False, allow_blank=True, default='')
    rashi = serializers.CharField(required=False, allow_blank=True, default='')
    is_manglik = serializers.BooleanField(required=False, allow_null=True)

    # --- Step 3: Education & Career ---
    education_level = serializers.CharField(required=False, allow_blank=True, default='')
    college = serializers.CharField(required=False, allow_blank=True, default='')
    occupation = serializers.CharField(required=False, allow_blank=True, default='')
    company = serializers.CharField(required=False, allow_blank=True, default='')
    annual_income = serializers.IntegerField(required=False, allow_null=True)
    work_location = serializers.CharField(required=False, allow_blank=True, default='')

    # --- Step 4: Family ---
    father_name = serializers.CharField(required=False, allow_blank=True, default='')
    father_occupation = serializers.CharField(required=False, allow_blank=True, default='')
    mother_name = serializers.CharField(required=False, allow_blank=True, default='')
    mother_occupation = serializers.CharField(required=False, allow_blank=True, default='')
    brothers_count = serializers.IntegerField(default=0)
    sisters_count = serializers.IntegerField(default=0)
    family_type = serializers.ChoiceField(choices=['joint', 'nuclear'], required=False, allow_blank=True)
    family_status = serializers.CharField(required=False, allow_blank=True, default='')

    # --- Step 5: Partner Preferences (nested) ---
    partner_preferences = PartnerPreferencesSerializer()

    # --- Step 6: Lifestyle + Location ---
    eating_habit = serializers.ChoiceField(choices=['veg', 'non_veg', 'vegan'], required=False, allow_blank=True)
    smoking_habit = serializers.ChoiceField(choices=['yes', 'no', 'occasionally'], required=False, allow_blank=True)
    drinking_habit = serializers.ChoiceField(choices=['no', 'occasionally', 'regular', 'daily'], required=False, allow_blank=True)
    hobbies = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    bio = serializers.CharField(required=False, allow_blank=True, default='')
    photo_privacy = serializers.ChoiceField(choices=['public', 'locked'], default='public')
    city = serializers.CharField(required=False, allow_blank=True, default='')
    state = serializers.CharField(required=False, allow_blank=True, default='')
    country = serializers.CharField(default='India')
    postal_code = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('This phone number is already registered.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email address is already registered.')
        return value

    def create(self, validated_data):
        prefs_data = validated_data.pop('partner_preferences')
        religion_id = validated_data.pop('religion_id', None)
        caste_id = validated_data.pop('caste_id', None)

        user_fields = {
            'phone_number': validated_data.pop('phone_number'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
        }

        with transaction.atomic():
            user = User.objects.create_user(**user_fields)

            religion = Religion.objects.get(id=religion_id) if religion_id else None
            caste = Caste.objects.get(id=caste_id) if caste_id else None

            Profile.objects.create(
                user=user,
                religion=religion,
                caste=caste,
                **validated_data,
            )

            PartnerPreferences.objects.create(user=user, **prefs_data)

        return user
