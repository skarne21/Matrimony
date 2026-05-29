from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.profiles.models import Profile, PartnerPreferences, Religion

User = get_user_model()

TEST_USERS = [
    {
        'phone_number': '+911111111111',
        'email': 'test1@veerabhadra.dev',
        'password': 'testpass123',
        'profile': {
            'first_name': 'Arjun',
            'last_name': 'Reddy',
            'gender': 'male',
            'dob': date(1996, 4, 15),
            'marital_status': 'never_married',
            'height_cm': 178,
            'mother_tongue': 'Telugu',
            'occupation': 'Software Engineer',
            'company': 'TCS',
            'education_level': 'B.Tech',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'country': 'India',
            'eating_habit': 'non_veg',
            'bio': 'Software engineer based in Hyderabad. Love cricket and travel.',
        },
        'prefs': {
            'age_min': 22, 'age_max': 30,
            'acceptable_religions': [], 'acceptable_castes': [],
        },
    },
    {
        'phone_number': '+912222222222',
        'email': 'test2@veerabhadra.dev',
        'password': 'testpass123',
        'profile': {
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'gender': 'female',
            'dob': date(1999, 8, 22),
            'marital_status': 'never_married',
            'height_cm': 163,
            'mother_tongue': 'Hindi',
            'occupation': 'Doctor',
            'company': 'Apollo Hospitals',
            'education_level': 'MBBS',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'country': 'India',
            'eating_habit': 'veg',
            'bio': 'Doctor at Apollo. Passionate about music and cooking.',
        },
        'prefs': {
            'age_min': 24, 'age_max': 34,
            'acceptable_religions': [], 'acceptable_castes': [],
        },
    },
]


class Command(BaseCommand):
    help = 'Seed two test users for local development'

    def handle(self, *args, **options):
        for entry in TEST_USERS:
            phone = entry['phone_number']

            if User.objects.filter(phone_number=phone).exists():
                self.stdout.write(f'  Skipped (already exists): {phone}')
                continue

            user = User.objects.create_user(
                phone_number=phone,
                email=entry['email'],
                password=entry['password'],
            )

            religion = Religion.objects.first()
            Profile.objects.create(user=user, religion=religion, **entry['profile'])
            PartnerPreferences.objects.create(user=user, **entry['prefs'])

            self.stdout.write(self.style.SUCCESS(f'  Created: {entry["profile"]["first_name"]} {entry["profile"]["last_name"]} ({phone})'))

        self.stdout.write('\nDone. Quick-login phones:')
        self.stdout.write('  Test 1 (male):   +911111111111')
        self.stdout.write('  Test 2 (female): +912222222222')
        self.stdout.write('OTP will print to the Django console as usual.')
