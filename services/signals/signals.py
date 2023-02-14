from turtle import pos
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from services.models import Location

@receiver(post_save,sender = get_user_model())
def create_location_for_new_user(sender,**kwargs):
    if kwargs['created']:
        Location.objects.create(user = kwargs['instance'])