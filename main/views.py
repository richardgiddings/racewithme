from django.shortcuts import render
from users.models import Profile
from .models import Race, UserRace
from .forms import UserProfileForm, RaceTargetsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from itertools import groupby
from datetime import date
from django.utils.html import conditional_escape as esc

@login_required
def user_profile(request):

    profile = Profile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)

    return render(request, template_name='main/user_profile.html', 
                  context={'form': form})

@login_required
def races(request):

    races = Race.objects.filter(race_date__gte=datetime.now()).order_by('race_date')

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
        user_race = UserRace.objects.create_user_race(request.user, race)
        user_race.status='1' # set to interested
        user_race.save()

    # get all UserRaces for user that they are interested in
    races = UserRace.objects.filter(user=request.user, status='1').order_by('race__race_date')
    
    return render(request, template_name='main/interested.html',
                  context={'races': races})

@login_required
def going(request):
    if request.method == 'POST':
        race_id = request.POST.get("race_id")
        race = Race.objects.get(pk=race_id)
        user_race = UserRace.objects.create_user_race(request.user, race)
        user_race.status = '2' # set to going
        user_race.save()

    races = UserRace.objects.filter(user=request.user, status='2').order_by('race__race_date')

    race_tuples = [(race, RaceTargetsForm(instance=race, auto_id='id_%s_'+str(race.id))) for race in races]

    return render(request, template_name='main/going.html',
                  context={'race_tuples': race_tuples})

@login_required
def no_longer_interested(request):

    race_id = request.POST.get("race_id")
    race = Race.objects.get(pk=race_id)
    user_race = UserRace.objects.get(user=request.user, race=race)
    user_race.delete()

    races = UserRace.objects.filter(user=request.user, status='1')

    return render(request, template_name='main/interested.html',
                  context={'races': races})

@login_required
def no_longer_going(request):

    race_id = request.POST.get("race_id")
    race = Race.objects.get(pk=race_id)
    user_race = UserRace.objects.get(user=request.user, race=race)
    user_race.delete()

    races = UserRace.objects.filter(user=request.user, status='2')

    return render(request, template_name="main/going.html",
                  context={'races': races})

@login_required
def completed(request):

    if request.method == 'POST':
        race_id = request.POST.get("race_id")
        race = Race.objects.get(pk=race_id)
        user_race = UserRace.objects.get(user=request.user, race=race)
        user_race.status = '3' # completed race
        user_race.save()

    races = UserRace.objects.filter(user=request.user, status='3').order_by('race__race_date')

    #cal = RaceCalendar(races).formatmonth(2017, 12)

    return render(request, template_name='main/completed.html',
                  context={'races': races })
                  #context={'races': races, 'calendar': mark_safe(cal)})

@login_required
def completed_race(request, id):
    race = UserRace.objects.get(pk=id)
    return render(request, template_name='main/completed_race.html',
                  context={'race': race})

@login_required
def set_target_time(request):

    if request.method == 'POST':
        race_id = request.POST.get("race_id")
        user_race = UserRace.objects.get(pk=race_id)
        form = RaceTargetsForm(request.POST, instance=user_race)

        if form.is_valid():
            form.save()
            
    return HttpResponseRedirect(reverse('going'))


class RaceCalendar(HTMLCalendar):

    def __init__(self, user_races):
        super(RaceCalendar, self).__init__()
        self.user_races = self.group_by_day(user_races)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass =+ ' today'
            if day in self.user_races:
                cssclass += ' filled'
                body = ['<ul>']
                for user_race in self.user_races[day]:
                    body.append('<li>')
                    body.append('<a href="%s">%s' % (user_race.get_absolute_url(), self.tooltip(user_race.race.race_name)))
                    body.append(esc(user_race.race.race_name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(RaceCalendar, self).formatmonth(year, month)

    def group_by_day(self, user_races):
        field = lambda user_race: user_race.race.race_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(user_races, field)]
        )

    def tooltip(self, body):
        return '<span class="tooltiptext">%s</span>' % body

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
