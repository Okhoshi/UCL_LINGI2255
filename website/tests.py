# -*- coding: cp1252 -*-
from django.test import TestCase
from models import *
import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext as _



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
                                                  password="azerty",
                                                  gender="M",
                                                  birth_day=datetime.datetime.utcnow().replace(tzinfo=utc)))
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
        au1 = AssociationUser.objects.create_user(username="au1", password="anz", email="i", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))
        au2 = AssociationUser.objects.create_user(username="au2", password="anzd", email="zi", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))
        au3 = AssociationUser.objects.create_user(username="au2-3", password="anzod", email="zoi", \
                              level=0, association=assoc[1], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))

        aua0 = assoc[0].get_employees()
        self.assertTrue(au1 in aua0)
        self.assertTrue(au2 in aua0)
        self.assertFalse(au3 in aua0)

    def test_associationuser_get_pin(self):
        assoc = ModelsTests.generate_association()
        au1 = AssociationUser.objects.create_user(username="au1", password="anz", email="i", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))
        au2 = AssociationUser.objects.create_user(username="au2", password="anzd", email="zi", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))
        au3 = AssociationUser.objects.create_user(username="au2-3", password="anzod", email="zoi", \
                              level=0, association=assoc[1], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))

        pin1 = PIN(first_name="hello", last_name="world", managed_by=au1)
        pin2 = PIN(first_name="bye", last_name="world", managed_by=au1)
        pin3 = PIN(first_name="hello", last_name="kitty", managed_by=au2)
        pin4 = PIN(first_name="bruce", last_name="willis", managed_by=au3)

        pin1.save()
        pin2.save()
        pin3.save()
        pin4.save()

        pin_au1 = au1.get_pin()

        self.assertTrue(pin1 in pin_au1)
        self.assertTrue(pin2 in pin_au1)
        self.assertFalse(pin3 in pin_au1)
        self.assertFalse(pin4 in pin_au1)

    def test_associationuser_set_pin(self):
        assoc = ModelsTests.generate_association()
        au1 = AssociationUser.objects.create_user(username="au1", password="anz", email="i", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))

        au1.set_pin(first_name="Georges", last_name="Bush")

        pin = au1.get_pin()[0]

        self.assertEqual("Georges", pin.first_name)
        self.assertEqual("Bush", pin.last_name)
        self.assertEqual(au1, pin.managed_by)

    def test_associationuser_get_pin(self):
        assoc = ModelsTests.generate_association()
        au1 = AssociationUser.objects.create_user(username="au1", password="anz", email="i", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))
        au2 = AssociationUser.objects.create_user(username="au2", password="anzd", email="zi", \
                              level=0, association=assoc[0], gender="F", birth_day=datetime.datetime.utcnow().replace(tzinfo=utc))

        pin1 = PIN(first_name="hello", last_name="world", managed_by=au1)
        pin2 = PIN(first_name="hello", last_name="kitty", managed_by=au1)

        pin1.save()
        pin2.save()

        au2.transfer_pin(pin=pin1, other_au=au2)
        au1.transfer_pin(pin=pin2, other_au=au2)

        self.assertEqual(pin1.managed_by, au1)
        self.assertEqual(pin2.managed_by, au2)
 
    
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

        self.assertEqual(",".join(map(lambda m: m.__unicode__(), message1)), ",".join(map(lambda m: m.__unicode__(), message2)))

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
                         rating_demander=3, rating_proposer=1)
        feed2 = Feedback(feedback_demander="It could be better", \
                         feedback_proposer="Very interesting!", request = req2,\
                         rating_demander=2, rating_proposer=2)

        feed1.save()
        feed2.save()

        self.assertEqual(users[0].get_rating(), (1, 0, 1))
        self.assertEqual(users[1].get_rating(), (0, 1, 1))




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

    def test_entity_get_similar_matching_requests(self):
        users = ModelsTests.generate_user()
        pla = Place()
        pla.save()
        
        req1 = Request(name="Je cherche 3 paires de chaussettes noires", category="Clothes", \
            place=pla, proposer=users[0], demander=users[1],\
            state=Request.DONE)
        req1.save()
        req2 = Request(name="J'ai faim et il me faudrait donc logiquement un nain de jardin", category="Food", place=pla,\
            proposer=users[0], demander=users[1], state=Request.DONE)
        req2.save()
        req3 = Request(name="J'organise un barbeque pour 10 personnes", category="Food", place=pla,\
            proposer=users[1], demander=users[0], state=Request.DONE)
        req3.save()
        req4 = Request(name="Bonjour, je donne un manteau et une paire de chaussures", category="Clothes",\
            place=pla, proposer=users[1], demander=users[0],\
            state=Request.DONE)
        req4.save()
        req5 = Request(name="J'ai besoin d'aide pour construire un meuble IKEA", category="Service",\
            place=pla, proposer=users[1], demander=users[0],\
            state=Request.DONE)
        req5.save()
        req6 = Request(name="J'offre 3h de tutorat si vous avez besoin d' aide en math ou physique", category="Service",\
            place=pla, proposer=users[1], demander=users[0],\
            state=Request.DONE)
        req6.save()
        req7 = Request(name="J'organise un paint-ball pour 12 personnes. Je fourni le materiel", category="Game", \
            place=pla, proposer=users[0], demander=users[1],\
            state=Request.DONE)
        req7.save()
        req8 = Request(name="Je cuisine un repas chaud pour 1 personne", category="Food", place=pla,\
            proposer=users[0], demander=users[1], state=Request.DONE)
        req8.save()
        req9 = Request(name="je cherche un manteau chaud pour l'hiver", category="Clothes", place=pla,\
            proposer=users[1], demander=users[0], state=Request.DONE)
        req9.save()
        req10 = Request(name="Salut, je cherche quelqu'un qui pourrait me conduire a un entretient d'embauche a Bruxelles", category="Service",\
            place=pla, proposer=users[1], demander=users[0],\
            state=Request.DONE)
        req10.save()
        req11 = Request(name="je donne 4 paires de chaussettes, des gants et deux bonnets", category="Clothes",\
            place=pla, proposer=users[1], demander=users[0],\
            state=Request.DONE)
        req11.save()
        req12 = Request(name="j'offre des vieux meubles : une armoire, une table et trois chaises", category="Furniture",\
            place=pla, proposer=users[1], demander=users[0],\
            state=Request.DONE)
        req12.save()

        prop1 = Request(name="Il me faudrait des nouveaux vetements pour l'hiver", category="Clothes", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop1.save()
        prop2 = Request(name="J'ai des vieux jeux PC a donner: Age of Empire 2, ...", category="Game", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop2.save()
        prop3 = Request(name="J'ai des vieux jeux PS a donner: Call of Duty, ...", category="Game", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop3.save()
        prop4 = Request(name="Echarpe rouge a donner", category="Clothes", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop4.save()
        prop5 = Request(name="Je cherche un pantalon chaud", category="Clothes", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop5.save()
        prop6 = Request(name="J'ai un peu de tout mais surtout pas de chaussettes noires il fait chaud", category="Clothes", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop6.save()
        prop7 = Request(name="Je voudrais un cafe chaud", category="Food", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop7.save()
        prop8 = Request(name="Buffet fruit et legumes de saison", category="Food", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop8.save()
        prop9 = Request(name="champignons de saison en rab. Il ont l'air un peu louches mais ils sont bons. Bon apres y'a un elephant rose qui essaye d'les voler", category="Food", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop9.save()
        prop10 = Request(name="j'ai besoin d'aide pour cuisiner un repas de noel pour 15 personnes", category="Service", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop10.save()
        prop11 = Request(name="Je peux vous aider a demenager. J'ai une camionnette assez grande pour la plupart des meubles", category="Service", place=pla,\
            proposer=users[1], demander=users[1], state=Request.PROPOSAL)
        prop11.save()

        res = users[0].get_similar_matching_requests(5)
        for i in res:
            print(i.name)

        self.assertTrue(len(res)==5)
        
        


    def test_entity_search(self):
        users = ModelsTests.generate_user()
        pla = Place()
        pla.save()
        savedsearch = SavedSearch(place = pla, date=\
            datetime.datetime.utcnow().replace(tzinfo=utc), search_field=\
            "Hello coucou bonjour oi salut wassup", category="test", \
            entity=users[0])
        savedsearch.save()

        req = Request(name="Hello cat dog llama duck", category="Test", \
            place=pla, proposer=users[0], demander=users[1],\
            state=Request.PROPOSAL)
        req2 = Request(name="Hello2", category="Test", place=pla,\
            proposer=users[1], demander=users[0], state=Request.DONE)
        req3 = Request(name="Goodbye", category="Not Test", place=pla,\
            proposer=users[1], demander=users[0], state=Request.PROPOSAL)
        req4 = Request(name="salut coucou dead beef boob", category="Test",\
            place=pla, proposer=users[1], demander=users[1],\
            state=Request.PROPOSAL)
        req5 = Request(name="oi wassup dead beef boob", category="Test",\
            place=pla, proposer=users[1], demander=users[1],\
            state=Request.PROPOSAL)
        req6 = Request(name="salut Hello bonjour beef boob", category="Test",\
            place=pla, proposer=users[1], demander=users[1],\
            state=Request.PROPOSAL)
        

        req.save()
        req2.save()
        req3.save()
        req4.save()
        req5.save()
        req6.save()

        res = users[0].search(savedsearch, 3)

        self.assertFalse(req in res)
        self.assertFalse(req2 in res)
        self.assertFalse(req3 in res)
        self.assertTrue(req4 in res)
        self.assertTrue(req5 in res)
        self.assertTrue(req6 in res)
        


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


    def test_entity_set_followed(self):
        users = ModelsTests.generate_user()
        users[0].set_followed(users[1])

        result = users[0].get_followed()
        self.assertEqual(result[0], users[1].entity_ptr)

    def test_filteredrequest_get_age_filter(self):
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
        freq = FilteredRequest(name="Hello", category="Test", place=pla, \
                               proposer=users[0])
        freq.save()
        age_req = AgeFilter(min_age=5, max_age=10, filtered_request=freq)
        age_req2 = AgeFilter(min_age=25, max_age=120, filtered_request=freq)

        age_req.save()
        age_req2.save()

        af = freq.get_age_filter()

        self.assertTrue(age_req in af)
        self.assertTrue(age_req2 in af)

    def test_filteredrequest_get_all_public_request(self):
        pla = Place()
        pla.save()
        users = ModelsTests.generate_user()
        req = Request(name="Hello", category="Test", place=pla, \
                      proposer=users[0], demander=users[1], state=Request.DONE)
        pla = Place()
        pla.save()
        freq = FilteredRequest(name="Hello", category="Test", place=pla, \
                               proposer=users[0])
        req.save()
        freq.save()

        public_req = FilteredRequest.get_all_public_requests()

        self.assertTrue(req in public_req)
        self.assertFalse(freq in public_req)


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
        self.assertEqual((users[0], _('Proposal')), req.get_initiator())
        self.assertEqual((users[1], _('Demand')), req2.get_initiator())

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

    def test_user_get_age(self):
        users = ModelsTests.generate_user(2)


        users[0].birth_day = datetime.datetime(2010, 05, 12).replace(tzinfo=utc)

        users[1].birth_day = datetime.datetime(2010, 12, 31).replace(tzinfo=utc)

        users[0].save()
        users[1].save()

        self.assertEqual(users[0].get_age(), 3)
        self.assertEqual(users[1].get_age(), 2)

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
        users = ModelsTests.generate_user(2)
        self.assertEquals(users[0].confirmed_status, users[0].is_verified())
        users[1].confirmed_status = True
        users[1].save()
        self.assertEquals(users[1].confirmed_status, users[1].is_verified())
        
