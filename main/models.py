from django.db import models


#class Race(models.Model):
"""
A Race listed on the website for people to join. This
contains the basic information about the race.
"""
#race_name = models.CharField()
#location = models.CharField()
# distance = models.CharField()
#race_site_link = models.URLField()

#class UserSettings(models.Model):
    

#class UserRace(models.Model):


class Distance(models.Model):
    description = models.CharField(max_length=25)

    def __str__(self):
        return self.description