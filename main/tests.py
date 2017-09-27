from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Race, UserRace, Location, Distance
from .forms import RaceTargetsForm

from datetime import datetime, timedelta

class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        # create some race locations
        cls.location1 = Location.objects.create(name="Bristol")
        cls.location2 = Location.objects.create(name="London")

        # create some race distances
        cls.distance1 = Distance.objects.create(description="10K")
        cls.distance2 = Distance.objects.create(description="Half Marathon")

        cls.today = datetime.now().date()
        cls.yesterday = cls.today - timedelta(1)

    def setUp(self):
        User.objects.create_user(username="user1", password="password1",
                                 email='mail@example.com')
        self.client.login(username='user1', password='password1')

    """
    Races Page
    """

    # see list of races
    def test_races_page_initial(self):

        # add a race
        race = Race.objects.create(
            race_name = "Race 1",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )

        race_old = Race.objects.create(
            race_name = "Race 2",
            race_location = self.location2,
            race_distance = self.distance2,
            race_site_link = "https://race-website.co.uk",
            race_date = self.yesterday,
            race_time = "12:10:24",
        )

        # check that a race appears on the races page
        response = self.client.get(reverse('races'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/races.html')

        # shows race today
        self.assertContains(response, "Race 1")
        # but doesn't show one from yesterday
        self.assertNotContains(response, "Race 2")

    # mark as interested
    def test_races_page_mark_interested(self):

        # add a race
        race = Race.objects.create(
            race_name = "Race 1",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )

        # go to races page
        response = self.client.get(reverse('races'))

        # 'click' the interested button
        response = self.client.post(
            reverse('interested'),
            data={ 'race_id': race.id },
            follow=True
        )

        # check that a userrace is created
        self.assertEqual(UserRace.objects.count(), 1)
        self.assertQuerysetEqual(response.context['races'], 
                                 ['<UserRace: Race 1>'])

        # check that we are on interested page
        self.assertTemplateUsed(response, 'main/interested.html')
        self.assertContains(response, "Race 1")


    # mark as going
    def test_races_page_mark_going(self):

        # add a race
        race = Race.objects.create(
            race_name = "Race 1",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )

        # go to races page
        response = self.client.get(reverse('races'))

        # 'click' the interested button
        response = self.client.post(
            reverse('going'),
            data={ 'race_id': race.id },
            follow=True
        )

        # check that a userrace is created
        self.assertEqual(UserRace.objects.count(), 1)
        self.assertQuerysetEqual(response.context['race_tuples'], 
            ['(<UserRace: Race 1>, <RaceTargetsForm bound=False, valid=Unknown, '
                                    'fields=(just_for_fun;target_hours;target_minutes;target_seconds)>)'])

        # check that we are on going page
        self.assertTemplateUsed(response, 'main/going.html')
        self.assertContains(response, "Race 1")

    """
    Interested Page
    """

    # list of races
    def test_interested_page_initial(self):
        # create a race and userrace
        race = Race.objects.create(
            race_name = "Interested Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='1',
            just_for_fun=True,
        )

        # go to interested page and check the race is there
        response = self.client.get(reverse('interested'))
        self.assertTemplateUsed(response, 'main/interested.html')
        self.assertQuerysetEqual(response.context['races'], 
                                 ['<UserRace: Interested Race>'])
        self.assertContains(response, 'Interested Race')

    # remove race
    def test_interested_page_remove_race(self):
        # add a race and a user race
        race = Race.objects.create(
            race_name = "Interested Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='1',
            just_for_fun=True,
        )

        # go to interested page
        response = self.client.get(reverse('interested'))

        # before marking the race as no longer interested 
        # we have a userrace entry
        self.assertEqual(UserRace.objects.count(), 1)

        # post to remove the race
        response = self.client.post(
            reverse('no_longer_interested'),
            data={'race_id': race.id},
            follow=True,
        )

        # the userrace is deleted
        self.assertEqual(UserRace.objects.count(), 0)
        # no races in context
        self.assertQuerysetEqual(response.context['races'], [])

    # mark as going
    def test_interested_page_mark_going(self):
        race = Race.objects.create(
            race_name = "Int to Going Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='1',
            just_for_fun=True,
        )

        # go to interested page
        response = self.client.get(reverse('interested'))

        # mark race as going
        response = self.client.post(
            reverse('going'),
            data={'race_id': race.id},
            follow=True,
        )

        # check that we are on going page and there is a 
        # userrace in the context
        self.assertTemplateUsed(response, 'main/going.html')
        self.assertQuerysetEqual(response.context['race_tuples'], 
            ['(<UserRace: Int to Going Race>, <RaceTargetsForm bound=False, valid=Unknown, '
            'fields=(just_for_fun;target_hours;target_minutes;target_seconds)>)'])

    """
    Going Page
    """

    # list of races
    def test_going_page_initial(self):
        # add a going race
        race = Race.objects.create(
            race_name = "Going Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='2',
            just_for_fun=True,
        )

        # check that it appears on going page
        response = self.client.get(reverse('going'))
        self.assertTemplateUsed(response, 'main/going.html')
        self.assertQuerysetEqual(response.context['race_tuples'],
            ['(<UserRace: Going Race>, <RaceTargetsForm bound=False, valid=Unknown, '
            'fields=(just_for_fun;target_hours;target_minutes;target_seconds)>)'])

    # remove race
    def test_going_page_remove_race(self):
       # add a race and a user race
        race = Race.objects.create(
            race_name = "Going Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='2',
            just_for_fun=True,
        )

        # go to going page
        response = self.client.get(reverse('going'))

        # before marking the race as no longer going 
        # we have a userrace entry
        self.assertEqual(UserRace.objects.count(), 1)

        # post to remove the race
        response = self.client.post(
            reverse('no_longer_going'),
            data={'race_id': race.id},
            follow=True,
        )

        # on going page
        self.assertTemplateUsed(response, 'main/going.html')

        # the userrace is deleted
        self.assertEqual(UserRace.objects.count(), 0)
        # no races in context
        self.assertQuerysetEqual(response.context['races'], [])

    # mark as completed 
    def test_going_page_mark_completed(self):
        race = Race.objects.create(
            race_name = "Going to Complete Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='2',
            just_for_fun=True,
        )

        # go to going page
        response = self.client.get(reverse('going'))

        # mark race as going
        response = self.client.post(
            reverse('completed'),
            data={'race_id': race.id},
            follow=True,
        )

        # check that we are on going page and there is a 
        # userrace in the context
        self.assertTemplateUsed(response, 'main/completed.html')
        self.assertQuerysetEqual(response.context['races'], 
                                 ['<UserRace: Going to Complete Race>'])

    # mark as just for fun
    #def test_going_page_mark_as_fun(self):
    #    pass

    # set targets
    #def test_going_page_set_targets(self):
    #    pass

    """
    Completed Page
    """

    # list of races
    def test_completed_page_intial(self):
        race = Race.objects.create(
            race_name = "Completed Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='3',
            just_for_fun=True,
        )

        # view completed race page
        response = self.client.get(reverse('completed'))
        self.assertTemplateUsed(response, 'main/completed.html')
        self.assertQuerysetEqual(response.context['races'], 
                                 ['<UserRace: Completed Race>'])

    # view individua race
    def test_ind_completed_page_initial(self):
        race = Race.objects.create(
            race_name = "Completed Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='3',
            just_for_fun=True,
        )

        # view individual completed race page
        response = self.client.get(reverse('completed_race', 
                    kwargs={ 'id': user_race.id }))
        self.assertTemplateUsed(response, 'main/completed_race.html')
        self.assertEqual(response.context['race'], user_race)

    
    def test_ind_completed_page_set_results(self):
        race = Race.objects.create(
            race_name = "Completed Race",
            race_location = self.location1,
            race_distance = self.distance1,
            race_site_link = "https://race-website.com",
            race_date = self.today,
            race_time = "12:10:24",
        )
        user = auth.get_user(self.client)
        user_race = UserRace.objects.create(
            user=user,
            race=race,
            status='3',
            just_for_fun=True,
        )

        # view individual completed race page
        response = self.client.get(reverse('completed_race', 
                                           kwargs={ 'id': user_race.id }))

        # get form
        form = response.context['results_form']
        data = form.initial

        # set achieved time
        data['achieved_hours'] = 2
        data['achieved_minutes'] = 3
        data['achieved_seconds'] = 4
        # set race results
        data['race_results_external'] = 'https://race-results.com'
        # set race photos
        data['race_photos_external'] = 'https://race-photos.net'

        # post the form
        data['race_id'] = user_race.id
        response = self.client.post(reverse('results_form'), 
                                    data,
                                    follow=True)
        
        # check results
        self.assertTemplateUsed(response, 'main/completed_race.html')
        self.assertContains(response, 'https://race-results.com')
        self.assertContains(response, 'https://race-photos.net')