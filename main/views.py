from django.shortcuts import render
from users.models import Profile, UserSettings
from .models import Race, UserRace
from users.models import User, Friend
from .forms import UserProfileForm, UserSettingsForm
from .forms import RaceTargetsForm, RaceResultsForm
from .forms import DistanceSelectionForm, RaceSuggestionForm
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

import django_rq
from .tasks import send_email
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_settings(user):
    settings, created = UserSettings.objects.get_or_create(
                            user=user,
                            defaults={
                                'just_username': False,
                                'use_default_distance': False,
                            }
                        )
    return settings

@login_required
def user_settings(request):

    settings = get_settings(request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.info(request, 'Settings changes have been saved.') 
    else:
        form = UserSettingsForm(instance=settings) 

    return render(request, template_name='main/user_settings.html',
                  context={'form': form})

@login_required
def user_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile changes have been saved.') 
    else:
        form = UserProfileForm(instance=profile)

    return render(request, template_name='main/user_profile.html', 
                  context={'form': form})

@login_required
def suggest_race(request):
    if request.method == 'POST':
        # go back to races page
        suggest_form = RaceSuggestionForm(request.POST)
        if suggest_form.is_valid():
            race_name = "Race name: '{}'".format(suggest_form.cleaned_data['race_name'])
            race_distance = "Race distance: {}".format(suggest_form.cleaned_data['race_distance'])
            race_date = "Race date: {:%d-%m-%Y}".format(suggest_form.cleaned_data['race_date'])
            race_time = "Race time: {}".format(suggest_form.cleaned_data['race_time'])

            # send email with form contents to admin
            # send email to user saying it has been sent to admin
            subject = "Race suggestion submitted"
            body = "The following race suggestion has been submitted.\n\n{}\n{}\n{}\n{}".format(
                    race_name, race_distance, race_date, race_time)

            # queue emails using redis
            queue = django_rq.get_queue('email')
            job = queue.enqueue(send_email, subject, body, [settings.DEFAULT_FROM_EMAIL])
            job = queue.enqueue(send_email, subject, body, [request.user.email])

            messages.info(request, "Your suggestion of '{}' has been sent.".format(
                                    suggest_form.cleaned_data['race_name']))

    else:
        # give form to user to fill in
        suggest_form = RaceSuggestionForm()

    return render(request, template_name='main/suggest_race.html',
                  context={'suggest_form': suggest_form})

@login_required
def races(request):

    # get the distance selected from the filter dropdown
    distance_id = request.GET.get('distance_list')
    if distance_id is None:
        distance_id = ''

    races = Race.objects.filter(race_date__gte=datetime.now()).order_by('race_date')
    user_races = UserRace.objects.filter(user=request.user)

    # filter the races if a distance is selected
    if distance_id != '':
        races = races.filter(race_distance__id=distance_id)
        user_races = user_races.filter(race__race_distance__id=distance_id)
    else:
        # get settings to see if we want to default to favourite distance
        settings = get_settings(request.user)
        if settings.use_default_distance:
            favourite_distance = request.user.profile.favourite_distance
            if favourite_distance is not None:
                distance_id = favourite_distance.id
                # set distance dropdown to favourite distance
                races = races.filter(race_distance__id=distance_id)
                user_races = user_races.filter(race__race_distance__id=distance_id)

    return_list = []
    for race in races:
        for user_race in user_races:
            if race.id == user_race.race.id:
                return_list.append((race, user_race.status_verbose()))
                break
        else:
            return_list.append((race, ''))

    # the distance filter dropdown
    distance_list = DistanceSelectionForm(initial={'distance_list': distance_id})

    # Add pagination
    paginator = Paginator(return_list, 5) # Show n races per page
    page = request.GET.get('page')
    try:
        return_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return_list = paginator.page(paginator.num_pages)

    return render(request, template_name='main/races.html',
                  context={'races': return_list, 'distance_list': distance_list})

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

    # Add pagination
    paginator = Paginator(races, 5) # Show n races per page
    page = request.GET.get('page')
    try:
        races = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        races = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        races = paginator.page(paginator.num_pages)

    return render(request, template_name='main/completed.html',
                  context={'races': races })

@login_required
def completed_race(request, id):
    race = UserRace.objects.get(pk=id)

    # get a list of friends who completed race too
    friends = request.user.profile.get_friends()

    friends_who_completed_race = []
    for friend in friends:
        # get completed races for the friend
        user_races = friend.get_races().filter(status='3')
        friends_races = [user_race.race.id for user_race in user_races]
        if race.race.id in friends_races:
            friends_who_completed_race.append(friend)

    results_form = RaceResultsForm(instance=race)

    return render(request, template_name='main/completed_race.html',
                  context={
                           'race': race, 
                           'results_form': results_form,
                           'friends_who_completed_race': friends_who_completed_race
                           })

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
    friends = request.user.profile.get_friends()

    return render(request, template_name='main/friends.html',
                  context={ 'friends': friends })

@login_required
def add_friend(request):

    email = request.POST.get('email')
    try:
        friend = User.objects.get(email=email)
    except ObjectDoesNotExist:
        messages.info(request, 'User does not exist.')
        return HttpResponseRedirect(reverse('friends'))

    # Can't add yourself!
    if request.user.id == friend.profile.user.id:
        messages.info(request, "That's you!")
        return HttpResponseRedirect(reverse('friends'))

    result = Friend.objects.filter(user_profile=request.user.profile, 
                                   friend_profile=friend.profile)

    if result:
        messages.info(request, 'They are already a friend.')
    else:
        Friend.objects.create(user_profile=request.user.profile, 
                              friend_profile=friend.profile)

        # get the new friend's name
        if friend.profile.first_name:
            display_name = "{} {}".format(friend.profile.first_name, 
                                          friend.profile.last_name)
        else:
            display_name = friend.username

        messages.info(request, '{} added.'.format(display_name))

        # send email
        already_friend = Friend.objects.filter(user_profile=friend.profile, 
                                                   friend_profile=request.user.profile)

        if request.user.profile.first_name:
            user_name = "{} {}".format(request.user.profile.first_name, 
                                       request.user.profile.last_name)
        else:
            user_name = request.user.username

        subject = "{} has added you as a friend".format(user_name)
        body = "{} has added you as a friend.\n".format(user_name)
        if not already_friend:
            body += "Why not add them to your friends to see which races they are signing up to."
        recipient_list = [friend.email,]

        # queue emails using redis
        queue = django_rq.get_queue('email')
        job = queue.enqueue(send_email, subject, body, recipient_list)

    return HttpResponseRedirect(reverse('friends'))

@login_required
def remove_friend(request):
    friend_id = request.POST.get('id', '')
    friend = Friend.objects.get(pk=friend_id)
    friend.delete()
    return HttpResponseRedirect(reverse('friends'))

@login_required
def friend_details(request, id):

    friend = Friend.objects.get(pk=id)
    user_races = friend.get_races()

    paginator = Paginator(user_races, 5) # Show n results per page
    page = request.GET.get('page')
    try:
        user_races = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_races = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_races = paginator.page(paginator.num_pages)

    return render(request, template_name='main/friend_details.html',
                  context={ 'friend': friend, 'user_races': user_races })
