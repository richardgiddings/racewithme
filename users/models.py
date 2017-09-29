from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Distance

class Profile(models.Model):
    user = models.OneToOneField(User, 
                               on_delete=models.CASCADE,
                               related_name="profile")
    email_confirmed = models.BooleanField(default=False)

    favourite_distance = models.ForeignKey(Distance,
                                    models.SET_NULL, 
                                    blank=True, 
                                    null=True)

    def get_friends(self):
        return Friend.objects.filter(user_profile=self)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Friend(models.Model):
    """
    Store friendship between a user and a friend
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    user_profile = models.ForeignKey(Profile, related_name="friend_user")
    friend_profile = models.ForeignKey(Profile, related_name="friend")