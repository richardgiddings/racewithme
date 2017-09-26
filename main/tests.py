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
        pass

    # mark as just for fun
    def test_going_page_mark_as_fun(self):
        pass

    # set targets
    def test_going_page_set_targets(self):
        pass

    # remove race
    def test_going_page_remove_race(self):
        pass

    # mark as completed 
    def test_going_page_mark_completed(self):
        pass

    """
    Completed Page
    """

    # list of races
    def test_completed_page_intial(self):
        pass

    # view individua race
    def test_ind_completed_page_intiail(self):
        pass

    # show hide details
    def test_ind_completed_page_show_details(self):
        pass

    # set achieved time
    def test_ind_completed_page_set_achieved_time(self):
        pass

    # set race results
    def test_ind_completed_page_set_race_results(self):
        pass

    # set race photos
    def test_ind_completed_page_set_race_photos(self):
        pass

