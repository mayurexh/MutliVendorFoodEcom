from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender = User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        print("User profile is created")
    else:
        try:
            profile = UserProfile.objects.get(user = instance)
            profile.save()
        except:
            #create profile if not exist
            UserProfile.objects.create(user = instance)
            print("Profile did not exist but we created")
        print("profile updated")



