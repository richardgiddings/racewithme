from django.db import models
from django.contrib.auth.models import User

#class UserSettings(models.Model):

RACE_STATUS = [
    ('0', 'Not Interested'), 
    ('1', 'Interested'), 
    ('2', 'Going'), 
    ('3', 'Completed'),
]

class UserRace(models.Model):
    """
    A race that a user is attending and the details
    for this user
    """
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
    target_hours = models.IntegerField()
    target_minutes = models.IntegerField()
    target_seconds = models.IntegerField()

    # time acheived
    achieved_hours = models.IntegerField()
    acheveed_minutes = models.IntegerField()
    achieved_seconds = models.IntegerField()

    # link to external race results and photos
    race_results_external = models.URLField()
    race_photos_external = models.URLField()

    # ADD PHOTO UPLOAD LATER !!!!!!!!

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