from django import forms
from users.models import Profile
from main.models import Distance, UserRace

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('favourite_distance',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['favourite_distance']=forms.ModelChoiceField(queryset=Distance.objects.all())

class RaceTargetsForm(forms.ModelForm):
    class Meta:
        model = UserRace
        fields = ('just_for_fun', 'target_hours', 'target_minutes', 'target_seconds')
        widgets = {
            'target_hours': forms.TextInput(attrs={'placeholder': 'hours'}),
            'target_minutes': forms.TextInput(attrs={'placeholder': 'minutes'}),
            'target_seconds': forms.TextInput(attrs={'placeholder': 'seconds'}),
        }