from website.models.user import *
from website.models.place import *
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        p = Place(country="Belgium", postcode=1348, city="LLN",
              street="Pl Ste Barbe", number=2)
        p.save()
        us = User.objects.create_user(args[0],  args[0] + "@me.SDI", "password", first_name=args[1], last_name=args[2],
                                      location=p,
                                      birth_day=datetime.today(),
                                      gender=User.MAN)