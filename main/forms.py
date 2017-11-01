from django import forms
from users.models import Profile
from main.models import Distance, UserRace, Race
from django.forms import extras
from racewithme.widgets.selecttimewidget import SelectTimeWidget

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'favourite_distance',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['favourite_distance']=forms.ModelChoiceField(queryset=Distance.objects.all())

class RaceSuggestionForm(forms.ModelForm):

    class Meta:
        model = Race
        fields = ('race_name', 'race_distance', 'race_site_link', 'race_date', 'race_time')
        widgets = {
            'race_date': extras.SelectDateWidget(
                            empty_label=("Choose Year", "Choose Month", "Choose Day"),
                        ),
            'race_time': SelectTimeWidget(twelve_hr=True)
        }

class RaceTargetsForm(forms.ModelForm):
    class Meta:
        model = UserRace
        fields = ('just_for_fun', 'target_hours', 'target_minutes', 'target_seconds')
        widgets = {
            'target_hours': forms.TextInput(attrs={'placeholder': 'h'}),
            'target_minutes': forms.TextInput(attrs={'placeholder': 'm'}),
            'target_seconds': forms.TextInput(attrs={'placeholder': 's'}),
        }

class RaceResultsForm(forms.ModelForm):
    class Meta:
        model = UserRace
        fields = (
            'achieved_hours', 
            'achieved_minutes', 
            'achieved_seconds',
            'race_results_external', 
            'race_photos_external')
        widgets = {
            'achieved_hours': forms.TextInput(attrs={'placeholder': 'h'}),
            'achieved_minutes': forms.TextInput(attrs={'placeholder': 'm'}),
            'achieved_seconds': forms.TextInput(attrs={'placeholder': 's'}),
            'race_results_external': forms.TextInput(attrs={'placeholder': 'link to results'}),
            'race_photos_external': forms.TextInput(attrs={'placeholder': 'link to photos'}),
        }

class DistanceSelectionForm(forms.Form):
    """
    A form to enable the filtering of races by distance
    """
    distance_list = forms.ModelChoiceField(queryset=Distance.objects.all(), 
                                           empty_label="All Distances",
                                           widget=forms.Select(attrs={"onChange":'this.form.submit()'}))
    distance_list.label = ''
    distance_list.required=False