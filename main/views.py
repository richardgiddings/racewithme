from django.shortcuts import render
from users.models import Profile
from .models import Race, UserRace
from users.models import User, Friend
from .forms import UserProfileForm, RaceTargetsForm, RaceResultsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from itertools import groupby
from datetime import date
from django.utils.html import conditional_escape as esc

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import EmailMessage
import sys
import threading


@login_required
def user_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save() 
    else:
        form = UserProfileForm(instance=profile)

    return render(request, template_name='main/user_profile.html', 
                  context={'form': form})

@login_required
def races(request):

    races = Race.objects.filter(race_date__gte=datetime.now()).order_by('race_date')
    user_races = UserRace.objects.filter(user=request.user)

    return_list = []
    for race in races:
        for user_race in user_races:
            if race.id == user_race.race.id:
                return_list.append((race, user_race.status_verbose()))
                break
        else:
            return_list.append((race, ''))


    return render(request, template_name='main/races.html',
                  context={'races': return_list})

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

    results_form = RaceResultsForm(instance=race)

    return render(request, template_name='main/completed_race.html',
                  context={'race': race, 'results_form': results_form })

@login_required
def set_target_time(request):

    if request.method == 'POST':
        race_id = request.POST.get("race_id")
        user_race = UserRace.objects.get(pk=race_id)
        form = RaceTargetsForm(request.POST, instance=user_race)

        if form.is_valid():
            form.save()
            
    return HttpResponseRedirect(reverse('going'))

@login_required
def results_form(request):

    if request.method == 'POST':
        race_id = request.POST.get("race_id")
        user_race = UserRace.objects.get(pk=race_id)
        form = RaceResultsForm(request.POST, instance=user_race)

        if form.is_valid():
            form.save()
            
    return HttpResponseRedirect(reverse('completed_race', 
                                        kwargs={ 'id': race_id }))

@login_required
def friends(request):
    # return friends list
    friends = request.user.profile.get_friends()
    friends_and_races = [(friend, friend.get_races()) for friend in friends]

    return render(request, template_name='main/friends.html',
                  context={ 'friends_and_races': friends_and_races })

@login_required
def add_friend(request):

    username = request.POST.get('username')
    try:
        friend = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.info(request, '{} does not exist.'.format(username))
        return HttpResponseRedirect(reverse('friends'))

    # Can't add yourself!
    if request.user.id == friend.profile.user.id:
        messages.info(request, "That's you!")
        return HttpResponseRedirect(reverse('friends'))

    result = Friend.objects.filter(user_profile=request.user.profile, 
                                   friend_profile=friend.profile)

    if result:
        messages.info(request, '{} is already a friend.'.format(username))
    else:
        Friend.objects.create(user_profile=request.user.profile, 
                              friend_profile=friend.profile)
        messages.info(request, '{} added.'.format(username))

        # send email
        try:
            already_friend = Friend.objects.filter(user_profile=friend.profile, 
                                                   friend_profile=request.user.profile)

            subject = "{} has added you as a friend".format(request.user.username)
            body = "{} has added you as a friend.\n".format(request.user.username)
            if not already_friend:
                body += "Why not add them to your friends to see which races they are signing up to."
            recipient_list = [friend.email,]

            EmailThread(subject, body, recipient_list).start()
        except Exception as detail:
            print >> sys.stderr, detail  

    return HttpResponseRedirect(reverse('friends'))

class EmailThread(threading.Thread):
    """
    Setup email functionality as a thread.
    """
    def __init__(self, subject, body, recipient_list):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(subject=self.subject, body=self.body, 
                           to=self.recipient_list)
        msg.send()

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
