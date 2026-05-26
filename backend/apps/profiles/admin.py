from django.contrib import admin
from .models import Religion, Caste, Profile, PartnerPreferences, ProfileView

admin.site.register(Religion)
admin.site.register(Caste)
admin.site.register(Profile)
admin.site.register(PartnerPreferences)
admin.site.register(ProfileView)
