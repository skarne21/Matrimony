from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex


class Religion(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'religions'

    def __str__(self):
        return self.name


class Caste(models.Model):
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name='castes')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'castes'

    def __str__(self):
        return f'{self.name} ({self.religion.name})'


class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'


class MaritalStatus(models.TextChoices):
    NEVER_MARRIED = 'never_married', 'Never Married'
    DIVORCED = 'divorced', 'Divorced'
    WIDOWED = 'widowed', 'Widowed'


class ProfileCreatedBy(models.TextChoices):
    SELF = 'self', 'Self'
    PARENT = 'parent', 'Parent'
    RELATIVE = 'relative', 'Relative'
    FRIEND = 'friend', 'Friend'


class EatingHabit(models.TextChoices):
    VEG = 'veg', 'Vegetarian'
    NON_VEG = 'non_veg', 'Non-Vegetarian'
    VEGAN = 'vegan', 'Vegan'


class SmokingHabit(models.TextChoices):
    YES = 'yes', 'Yes'
    NO = 'no', 'No'
    OCCASIONALLY = 'occasionally', 'Occasionally'


class DrinkingHabit(models.TextChoices):
    NO = 'no', 'No'
    OCCASIONALLY = 'occasionally', 'Occasionally'
    REGULAR = 'regular', 'Regular'
    DAILY = 'daily', 'Daily'


class FamilyType(models.TextChoices):
    JOINT = 'joint', 'Joint'
    NUCLEAR = 'nuclear', 'Nuclear'


class PhotoPrivacy(models.TextChoices):
    PUBLIC = 'public', 'Public'
    LOCKED = 'locked', 'Locked'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    # Basic info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    dob = models.DateField()
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices)
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.PositiveIntegerField(null=True, blank=True)
    profile_created_by = models.CharField(max_length=20, choices=ProfileCreatedBy.choices, default=ProfileCreatedBy.SELF)

    # Personal / religion
    mother_tongue = models.CharField(max_length=100, blank=True)
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, null=True, blank=True)
    caste = models.ForeignKey(Caste, on_delete=models.SET_NULL, null=True, blank=True)
    sub_caste = models.CharField(max_length=100, blank=True)
    nakshatra = models.CharField(max_length=100, blank=True)
    rashi = models.CharField(max_length=100, blank=True)
    is_manglik = models.BooleanField(null=True, blank=True)

    # Education & career
    education_level = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=200, blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    annual_income = models.PositiveIntegerField(null=True, blank=True)
    work_location = models.CharField(max_length=200, blank=True)

    # Family
    father_name = models.CharField(max_length=200, blank=True)
    father_occupation = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    mother_occupation = models.CharField(max_length=200, blank=True)
    brothers_count = models.PositiveSmallIntegerField(default=0)
    sisters_count = models.PositiveSmallIntegerField(default=0)
    family_type = models.CharField(max_length=10, choices=FamilyType.choices, blank=True)
    family_status = models.CharField(max_length=200, blank=True)

    # Lifestyle
    eating_habit = models.CharField(max_length=10, choices=EatingHabit.choices, blank=True)
    smoking_habit = models.CharField(max_length=15, choices=SmokingHabit.choices, blank=True)
    drinking_habit = models.CharField(max_length=15, choices=DrinkingHabit.choices, blank=True)
    hobbies = models.JSONField(default=list, blank=True)

    # Profile content
    bio = models.TextField(blank=True)
    profile_pic_url = models.CharField(max_length=500, blank=True)
    id_proof_url = models.CharField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    photo_privacy = models.CharField(max_length=10, choices=PhotoPrivacy.choices, default=PhotoPrivacy.PUBLIC)

    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'
        indexes = [
            # Composite index: search queries filter on all three simultaneously
            models.Index(fields=['religion', 'caste', 'gender'], name='idx_religion_caste_gender'),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PartnerPreferences(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partner_preferences',
    )
    age_min = models.PositiveSmallIntegerField(default=18)
    age_max = models.PositiveSmallIntegerField(default=60)
    height_min_cm = models.PositiveIntegerField(null=True, blank=True)
    height_max_cm = models.PositiveIntegerField(null=True, blank=True)
    # JSONB arrays of IDs — GIN indexed for overlap queries
    acceptable_religions = models.JSONField(default=list, blank=True)
    acceptable_castes = models.JSONField(default=list, blank=True)
    preferred_education = models.CharField(max_length=200, blank=True)
    preferred_profession = models.CharField(max_length=200, blank=True)
    preferred_location = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'partner_preferences'
        indexes = [
            GinIndex(fields=['acceptable_religions'], name='idx_gin_acceptable_religions'),
            GinIndex(fields=['acceptable_castes'], name='idx_gin_acceptable_castes'),
        ]

    def __str__(self):
        return f'Preferences for {self.user}'


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_views_given',
    )
    viewed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_views_received',
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'profile_views'
