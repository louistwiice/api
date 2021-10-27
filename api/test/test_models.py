from django.test import TestCase
from rest_framework.test import APITestCase
from api.models import *

# Create your tests here.

class ApiTest(TestCase):
    """ Test for api models """

    @classmethod
    def setUpTestData(cls):
        FitnessProgram.objects.create(
            name="Remise en forme",
            duree=30,
            target="B",
            description="Il s'agit d'un programme simple juste pour les gens souhaitant faire du sport par plaisir\nPour toute categorie de personnes"
        )


    def setUp(self):
        client = Userstype.objects.create(user_type="Client")
        docteur= Userstype.objects.create(user_type="Docteur")
        coach = Userstype.objects.create(user_type="Coach")

        self.admin= Account.objects.create_superuser(
            email="admin@mail.com",
            username="admin",
            firstname="Admin",
            lastname="Fitness",
            password="admin123456789"
        )

        self.michel= Account.objects.create_user(
            email="michel@mail.com",
            username="michel",
            firstname="Michel",
            lastname="Richardo",
            password="michel123456789",
            phone="+221701230738",
            user_type= coach
        )

        self.jasmine= Account.objects.create_user(
            email="jasmine@mail.com",
            username="jasmine",
            firstname="Jasmine",
            lastname="Ndour",
            password="jasmine123456789",
            user_type= client
        )

        self.amina= Account.objects.create_user(
            email="aminata@mail.com",
            username="aminata",
            firstname="aminata",
            lastname="Duboi",
            password="aminata123456789",
            user_type=docteur
        )



    def test_ratings_customers(self):
        AccountRating.objects.create(account=self.michel, account_to_rate=self.amina, stars=4)
        AccountRating.objects.create(account=self.jasmine, account_to_rate=self.amina, stars= 5)

        #A user account rate should be visible with number_of_rating, avg_rating
        self.assertEqual(self.amina.number_of_rating(), 2)
        self.assertEqual(self.amina.avg_rating(), 4.5)

        # A user account without rate should have rate equal to 0
        self.assertEqual(self.michel.number_of_rating(), 0)
        self.assertEqual(self.michel.avg_rating(), 0)


    # def test_account_rating_another_account_two_time_should_not_pass(self):
    #     AccountRating.objects.create(account=self.michel, account_to_rate=self.amina, stars=4)
    #     AccountRating.objects.create(account=self.michel, account_to_rate=self.amina, stars=5)

