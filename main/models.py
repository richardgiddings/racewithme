from django.db import models
from django.contrib.auth.models import User

#class UserSettings(models.Model):

RACE_STATUS = [
    ('0', 'Not Interested'), 
    ('1', 'Interested'), 
    ('2', 'Going'), 
    ('3', 'Completed'),
]

class UserRaceManager(models.Manager):
    """
    Manage the creation of user races
    """
    def create_user_race(self, user, race):
        user_race, created = self.get_or_create(user=user, race=race, 
                                defaults={'just_for_fun': True})
        return user_race

class UserRace(models.Model):
    """
    A race that a user is attending and the details
    for this user
    """
    objects = UserRaceManager()

    user = models.ForeignKey(
                        User,
                        models.SET_NULL,
                        blank=True,
                        null=True)
    race = models.ForeignKey(
                        'Race',
                        models.SET_NULL,
                        blank=True,
                        null=True)

    # status of race
    status = models.CharField(max_length=14, choices=RACE_STATUS, default='0')

    # no times if this ticked
    just_for_fun = models.BooleanField()
    
    # target time
    target_hours = models.IntegerField(blank=True, null=True)
    target_minutes = models.IntegerField(blank=True, null=True)
    target_seconds = models.IntegerField(blank=True, null=True)

    # time acheived
    achieved_hours = models.IntegerField(blank=True, null=True)
    acheveed_minutes = models.IntegerField(blank=True, null=True)
    achieved_seconds = models.IntegerField(blank=True, null=True)

    # link to external race results and photos
    race_results_external = models.URLField()
    race_photos_external = models.URLField()

    # ADD PHOTO UPLOAD LATER !!!!!!!!

    def __str__(self):
        return race.race_name

class Race(models.Model):
    """
    A Race listed on the website for people to join. This
    contains the basic information about the race.
    """
    race_name = models.CharField(max_length=50)
    race_location = models.ForeignKey(
                                'Location', 
                                models.SET_NULL, 
                                blank=True, 
                                null=True)
    race_distance = models.ForeignKey(
                                'Distance', 
                                models.SET_NULL, 
                                blank=True, 
                                null=True)
    race_site_link = models.URLField()
    race_date = models.DateField()
    race_time = models.TimeField()

    def __str__(self):
        return self.race_name

class Location(models.Model):
    """
    A Race location
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Distance(models.Model):
    """
    A race distance
    """
    description = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.description