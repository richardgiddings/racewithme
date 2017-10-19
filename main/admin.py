from django.contrib import admin
from .models import Distance, Race, UserRace

admin.site.register(Distance)
admin.site.register(Race)
admin.site.register(UserRace)