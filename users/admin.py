from django.contrib import admin
from .models import Profile, Friend
from .forms import SignUpForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class EmailRequiredUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = SignUpForm
    add_fieldsets = ((None, {'fields': ('username', 'email',
                                        'password1', 'password2'), 'classes': ('wide',)}),)
admin.site.unregister(User)
admin.site.register(User, EmailRequiredUserAdmin)

class FriendInline(admin.StackedInline):
    model = Friend
    fk_name = "user_profile"
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    inlines=[FriendInline]

admin.site.register(Profile, ProfileAdmin)