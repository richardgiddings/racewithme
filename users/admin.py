from django.contrib import admin
from .models import Profile, Friend

class FriendInline(admin.StackedInline):
    model = Friend
    fk_name = "user_profile"
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    inlines=[FriendInline]

admin.site.register(Profile, ProfileAdmin)