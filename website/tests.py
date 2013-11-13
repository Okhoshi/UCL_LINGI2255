from django.test import TestCase
from models import *

# Create your tests here.
class ModelsTests(TestCase):

    def test_testimony_get_random(self):
        # TO BE ENHANCED!
        testimonies = Testimony(testimony="Hello, I'm sexy and I know it!")
        self.assertEqual(testimonies.testimony,"Hello, I'm sexy and I know it!")
