from django.core.management.base import BaseCommand, CommandError
from neversets.utils import friends_update
from neversets.models import UserProfile
import datetime

class Command(BaseCommand):

    help = 'Sends weekly email to users'

    def handle(self, *args, **options):
    	user = UserProfile.objects.get(email="jonathan.cox.c@gmail.com")
    	friends_update(user)
#        if datetime.datetime.today().weekday() == 4:
#            for user in UserProfile.objects.all():
# 	        email(user)
