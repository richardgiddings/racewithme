from django import forms
from users.models import Profile
from main.models import Distance

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('favourite_distance',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['favourite_distance']=forms.ModelChoiceField(queryset=Distance.objects.all())