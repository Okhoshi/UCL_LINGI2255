from django.test import TestCase
from models import *
import datetime
from django.utils.timezone import utc



# Create your tests here.
class ModelsTests(TestCase):

    @staticmethod
    def generate_user(number=2):
        users = []
        for index in range(number):
            pla = Place()
            pla.save()
            users.append(User.objects.create_user(first_name="W"+str(index), \
                                                  last_name="User",\
                                                  location=pla, \
                                                  confirmed_status=True,\
                                                  username="E"+str(index),\
                                                  email="ci@ici.be",\
                                                  password="azerty"))
        return users

    @staticmethod
    def generate_association(number=2):
        association = []
        for index in range(number):
            pla = Place()
            pla.save()
            association.append(Association(name="W"+str(index), \
                                           description="Youpoie", location=pla))
            association[index].save()
        return association

    def test_association_get_employees(self):
        assoc = ModelsTests.generate_association()
        au1 = AssociationUser(username="au1", password="anz", email="i", \
                              level=0, association=assoc[0])
        au2 = AssociationUser(username="au2", password="anzd", email="zi", \
                              level=0, association=assoc[0])
        au3 = AssociationUser(username="au2-3", password="anzod", email="zoi", \
                              level=0, association=assoc[1])

        au1.save()
        au2.save()
        au3.save()

        aua0 = assoc[0].get_employees()
        self.assertTrue(au1 in aua0)
        self.assertTrue(au2 in aua0)
        self.assertFalse(au3 in aua0)
    
    def test_entity_get_all_requests(self):
        users =  ModelsTests.generate_user()
        pla = Place()
        pla.save()
        req = Request(name="Hello kitty", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        req2 = Request(name="Kim M. gives a sock", category="Test", place=pla, \
                      proposer=users[1], demander=users[0], state=Request.DONE)
        req2.save()
        req3 = Request(name="Who want to play planning poker?", category="Test", place=pla, \
                       demander=users[1])
        req3.save()

        requests = users[0].get_all_requests()
        self.assertTrue(req in requests) 
        self.assertTrue(req2 in requests)
        self.assertFalse(req3 in requests)


    def test_entity_get_current_requests(self):
        users =  ModelsTests.generate_user()
        pla = Place()
        pla.save()
        req = Request(name="Hello 1", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.IN_PROGRESS)
        req.save()
        req2 = Request(name="Hello 2", category="Test", place=pla, \
                      proposer=users[1], demander=users[0], state=Request.IN_PROGRESS)
        req2.save()
        req3 = Request(name="Hello 3", category="Test", place=pla, \
                       proposer=users[0], demander=users[1], state=Request.DONE)
        req3.save()
        req4 = Request(name="Hello 4", category="Test", place=pla, \
                       proposer=users[1])
        req4.save()

        requests = users[0].get_current_requests()
        self.assertTrue(req in requests) 
        self.assertTrue(req2 in requests)
        self.assertFalse(req3 in requests)
        self.assertFalse(req4 in requests)



        
    def test_entity_get_feedback(self):
        users = ModelsTests.generate_user(number=3)
        pla = Place()
        pla.save()
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
        req6 = Request(name="Bouffi2", category="Test", place=pla, \
                      proposer=users[1], demander=users[2], state=Request.DONE)

        req3.save()
        req4.save()
        req5.save()
        req6.save()

        feed1 = Feedback(feedback_demander="It was nice", \
                         feedback_proposer="It was ugly!", request = req, \
                         rating_demander=5, rating_proposer=1)
        feed2 = Feedback(feedback_demander="It could be better", \
                         feedback_proposer="Very interesting!", request = req2,\
                         rating_demander=2, rating_proposer=4)
        feed3 = Feedback(feedback_demander="Nice!", \
                         feedback_proposer="Wonderful!", request = req3, \
                         rating_demander=4, rating_proposer=5)
        feed4 = Feedback(feedback_demander="Nicer!", \
                         feedback_proposer="Wonderfuler!", request = req6, \
                         rating_demander=4, rating_proposer=5)

        feed1.save()
        feed2.save()
        feed3.save()
        feed4.save()

        feedu0 = users[0].get_feedback()
        self.assertFalse(feed1 in feedu0[0])
        self.assertTrue(feed1 in feedu0[1])
        self.assertFalse(feed2 in feedu0[0])
        self.assertTrue(feed2 in feedu0[1])
        self.assertTrue(feed3 in feedu0[0])
        self.assertFalse(feed3 in feedu0[1])
        self.assertFalse(feed4 in feedu0[0])
        self.assertFalse(feed4 in feedu0[1])

    def test_entity_get_internal_messages(self):
        users = ModelsTests.generate_user()
        pla = Place()
        pla.save()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        internal_message = InternalMessage(time = datetime.datetime.utcnow().replace(tzinfo=utc),\
            sender = users[0],request=req , message = "Coucou, voici une chaussette !",\
            receiver = users[1])
        internal_message.save()

        message1 = users[0].get_internal_messages(req)
        message2 = users[1].get_internal_messages(req)

        self.assertEqual(",".join(map(lambda m: m.__unicode__(), message1)),",".join(map(lambda m: m.__unicode__(), message2)))

    def test_entity_get_old_requests(self):
        users =  ModelsTests.generate_user()
        pla = Place()
        pla.save()
        req = Request(name="Hello 1", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        req2 = Request(name="Hello 2", category="Test", place=pla, \
                      proposer=users[1], demander=users[0], state=Request.DONE)
        req2.save()
        req3 = Request(name="Hello 3", category="Test", place=pla, \
                       proposer=users[0], demander=users[1], state=\
                       Request.IN_PROGRESS)
        req3.save()
        req4 = Request(name="Hello 4", category="Test", place=pla, \
                       proposer=users[1])
        req4.save()

        requests = users[0].get_old_requests()
        self.assertTrue(req in requests) 
        self.assertTrue(req2 in requests)
        self.assertFalse(req3 in requests)
        self.assertFalse(req4 in requests)

    def test_entity_get_rating(self):
        users = ModelsTests.generate_user()
        pla = Place()
        pla.save()

        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      proposer=users[1], demander=users[0], state=Request.DONE)
        req.save()
        req2.save()

        feed1 = Feedback(feedback_demander="It was nice", \
                         feedback_proposer="It was ugly!", request = req, \
                         rating_demander=5, rating_proposer=1)
        feed2 = Feedback(feedback_demander="It could be better", \
                         feedback_proposer="Very interesting!", request = req2,\
                         rating_demander=2, rating_proposer=4)

        feed1.save()
        feed2.save()

        self.assertEqual(users[0].get_rating(), 4.5)




    def test_entity_get_searches(self):
        users = ModelsTests.generate_user()
        pla = Place()
        pla.save()
        savedsearch = SavedSearch(place=pla, date=\
            datetime.datetime.utcnow().replace(tzinfo=utc), search_field=\
            "hello", category="test", entity=users[0])
        savedsearch.save()

        result0 = users[0].get_searches()
        result1 = users[1].get_searches()

        self.assertTrue(savedsearch in result0)
        self.assertFalse(savedsearch in result1)


    def test_entity_send_internal_message(self):
        users = ModelsTests.generate_user()
        pla = Place()
        pla.save()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        users[0].send_internal_message(request=req, text=\
            "Coucou, do you want to meet me?", destination_entity=users[1])
        result1 = users[0].get_internal_messages(req)
        result2 = users[1].get_internal_messages(req)

        self.assertEqual(result1[0], result2[0])
        self.assertEqual(result1[0].message, "Coucou, do you want to meet me?") 


    def  test_entity_set_followed(self):
        users = ModelsTests.generate_user()
        users[0].set_followed(users[1])

        result = users[0].get_followed()
        self.assertEqual(result[0], users[1].entity_ptr)
        

    def test_request_get_all_requests(self):
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        req.save()
        req2.save()
        all_req = Request.get_all_requests()
        self.assertTrue(req in all_req)
        self.assertTrue(req2 in all_req)

    def test_request_get_feedback(self):
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        feedback = Feedback(feedback_demander="Heeee", \
                            feedback_proposer="Shit", request=req, \
                            rating_proposer=3, rating_demander=1)
        feedback2 = req.get_feedback()
        self.assertEqual(feedback, feedback2)

    def test_request_get_initiator(self):
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], state=Request.PROPOSAL)
        req2 = Request(name="Hello2", category="Test", place=pla, \
                      demander=users[1], state=Request.PROPOSAL)
        req.save()
        req2.save()
        self.assertEqual(users[0], req.get_initiator())
        self.assertEqual(users[1], req2.get_initiator())

    def test_request_get_similar_requests(self):
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
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
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
            
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

    def test_user_is_verified(self):
        user = ModelsTests.generate_user(1)
        self.assertEquals(user[0].confirmed_status, user[0].is_verified())
        pla = Place()
        pla.save()
        user2 = User.objects.create_user(first_name="W64", \
                                         last_name="User",\
                                         location = pla, \
                                        username="E32", \
                                         email="ci@ici.be",\
                                         password="azerty")
        self.assertEquals(user2.confirmed_status, user2.is_verified())
        
