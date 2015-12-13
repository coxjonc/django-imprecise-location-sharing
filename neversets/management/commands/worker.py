from django.core.management.base import BaseCommand
from neversets.utils import friends_update
from neversets.models import UserProfile
import datetime

class Command(BaseCommand):

    help = 'Sends weekly email to users'

    def handle(self, *args, **options):
        if datetime.datetime.today().weekday() == 6:
            for user in UserProfile.objects.all():
                friends_update(user)
