from django.test import TestCase
from models import *

# Create your tests here.
class ModelsTests(TestCase):

    def test_testimony_get_random(self):
        # Creation
        testimony1 = Testimony(testimony="Hello, I'm sexy and I know it!")
        self.assertEqual(testimony1.testimony,"Hello, I'm sexy and I know it!")
        testimony2 = Testimony(testimony="Hi, glad to meet you...")
        self.assertEqual(testimony2.testimony,"Hi, glad to meet you...")
        testimony3 = Testimony(testimony="I'm the best of the world")
        self.assertEqual(testimony3.testimony,"I'm the best of the world")
        # Save in database
        testimony1.save()
        testimony2.save()
        testimony3.save()
        # Now test it!
        print(Testimony.get_random_testimonies(1))
        print(Testimony.get_random_testimonies(2))
        print(Testimony.get_random_testimonies(2))
        print(Testimony.get_random_testimonies(4))
