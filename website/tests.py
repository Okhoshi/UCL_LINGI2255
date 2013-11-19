from django.test import TestCase
from models import *
import datetime
from django.utils.timezone import utc



# Create your tests here.
class ModelsTests(TestCase):

    def test_entity_get_feedback(self):
        users = []
        for index in range(2):
            pla = Place()
            pla.save()
            users.append(User(first_name="W"+str(index), last_name="User", \
                                location=pla, confirmed_status=True \
                              username="E"+str(index)))
            users[index].save()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        req2.save()
        req3 = Request(name="Bouffi", category="Test", place=pla, \
                      proposer=users[1], demander=users[0], state=Request.DONE)
        req4 = Request(name="Coco", category="Plante", place=pla, \
                      demander=users[0], state=Request.IN_PROGRESS)
        req5 = Request(name="World: hello!", category="Plante", place=pla, \
                      demander=users[0], state=Request.PROPOSAL)

        req3.save()
        req4.save()
        req5.save()

        feed1 = Feedback(feedback_demander="It was nice", \
                         feedback_proposer="It was ugly!", request = req, \
                         rating_demander=5, rating_proposer=1)
        feed2 = Feedback(feedback_demander="It could be better", \
                         feedback_proposer="Very interesting!", request = req2,\
                         rating_demander=2, rating_proposer=4)
        feed3 = Feedback(feedback_demander="Nice!", \
                         feedback_proposer="Wonderful!", request = req3, \
                         rating_demander=4, rating_proposer=5)

        feed1.save()
        feed2.save()
        feed3.save()

        print(users[0].get_feedback())

    def test_request_get_all_requests(self):
        users = []
        for index in range(2):
            pla = Place()
            pla.save()
            users.append(User(first_name="E"+str(index), last_name="User", \
                                location=pla, confirmed_status=True, \
                              username="E"+str(index)))
            users[index].save()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        req2.save()
        print(Request.get_all_requests())

    def test_request_get_feedback(self):
        pla = Place()
        users = []
        for index in range(2):
            users.append(User(first_name="E"+str(index), last_name="User", \
                                location=pla, confirmed_status=True)) 
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        feedback = Feedback(feedback_demander="Heeee", \
                            feedback_proposer="Shit", request=req, \
                            rating_proposer=3, rating_demander=1)
        feedback2 = req.get_feedback()
        self.assertEqual(feedback, feedback2)
        print(feedback)
        print(feedback2)

    def test_request_get_initiator(self):
        users = []
        for index in range(2):
            pla = Place()
            pla.save()
            users.append(User(first_name="E"+str(index), last_name="User", \
                                location=pla, confirmed_status=True, \
                              username="E"+str(index)))
            users[index].save()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], state=Request.PROPOSAL)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      demander=users[1], state=Request.PROPOSAL)
        req.save()
        req2.save()
        self.assertEqual(users[0], req.get_initiator())
        self.assertEqual(users[1], req2.get_initiator())

    def test_request_get_similar_requests(self):
        users = []
        for index in range(2):
            pla = Place()
            pla.save()
            users.append(User(first_name="E"+str(index), last_name="User", \
                                location=pla, confirmed_status=True, \
                              username="E"+str(index)))
            users[index].save()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        req2.save()
        req3 = Request(name="Bouffi", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req4 = Request(name="Coco", category="Plante", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req5 = Request(name="World: hello!", category="Plante", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)

        req3.save()
        req4.save()
        req5.save()
        print(req.get_similar_requests())

    def test_request_make_request(self):
        users = []
        for index in range(2):
            pla = Place()
            pla.save()
            users.append(User(first_name="E"+str(index), last_name="User", \
                                location=pla, confirmed_status=True, \
                              username="E"+str(index)))
            users[index].save()
            
        coco_search = SavedSearch(entity=users[0], \
                            date=datetime.datetime.utcnow().replace(tzinfo=utc), \
                                  search_field="Hello world", category="Test", \
                                  place = pla)
        pla = Place()
        pla.save()
        coco_search2 = SavedSearch(entity=users[1], \
                            date=datetime.datetime.utcnow().replace(tzinfo=utc),\
                                  search_field="Lonely days", category="Test", \
                                  place = pla)
        coco_search.save()
        coco_search2.save()

        req1 = Request.make_request(coco_search, False)
        req2 = Request.make_request(coco_search2, True)

        self.assertEqual(coco_search.entity, req1.demander)
        self.assertEqual(coco_search.search_field, req1.name)
        self.assertEqual(coco_search.date, req1.date)
        self.assertEqual(coco_search.place, req1.place)
        self.assertEqual(coco_search.category, req1.category)
        self.assertEqual(coco_search2.entity, req2.proposer)
        self.assertEqual(coco_search2.search_field, req2.name)
        self.assertEqual(coco_search2.date, req2.date)
        self.assertEqual(coco_search2.place, req2.place)
        self.assertEqual(coco_search2.category, req2.category)

        

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
        for i in range(1,5):
            t1 = Testimony.get_random_testimonies(i)
            print(t1)
            self.assertEqual(len(t1), min(i, Testimony.objects.count()))

                            
