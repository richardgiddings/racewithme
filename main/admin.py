from django.contrib import admin
from .models import Distance, Location, Race, UserRace

admin.site.register(Distance)
admin.site.Register(Location)
admin.site.register(Race)
admin.site.register(UserRace)