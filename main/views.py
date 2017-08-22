from django.shortcuts import render
from users.models import Profile
from .models import Race
from .forms import UserProfileForm

def user_profile(request):

    profile = Profile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)

    return render(request, template_name='main/user_profile.html', 
                  context={'form': form})

def races(request):

    races = Race.objects.all()
    races = Race.order_by('')

    return render(request, template_name='main/races.html',
                  context={'races': races})