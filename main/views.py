from django.shortcuts import render
from users.models import Profile
from .models import Race, UserRace
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):

    profile = Profile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)

    return render(request, template_name='main/user_profile.html', 
                  context={'form': form})

@login_required
def races(request):

    races = Race.objects.all()
    races = Race.objects.order_by('race_date')

    # filter out races that the user has already expressed interest in
    user_races = UserRace.objects.filter(user=request.user).values_list('race', flat=True)
    races = [race for race in races if race.id not in user_races]

    return render(request, template_name='main/races.html',
                  context={'races': races})

@login_required
def interested(request):
    if request.method == 'POST':
        # create a new UserRace instance pointing to Race for User
        race_id = request.POST.get("race_id")
        race = Race.objects.get(pk=race_id)
        user_race = UserRace.objects.create_user_race(
            request.user, race, '1')

    # get all UserRaces for user that they are interested in
    races = UserRace.objects.filter(user=request.user)
    races = races.filter(status='1')
    
    return render(request, template_name='main/interested.html',
                  context={'races': races})