from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import *
import json
from ..serializers import *


class UserLoginTest(TestCase):


    def setUp(self):
        client = Userstype.objects.create(user_type="Client")
        docteur = Userstype.objects.create(user_type="Docteur")
        coach = Userstype.objects.create(user_type="Coach")

        self.michel = Account.objects.create_user(
            email="michel@mail.com",
            username="michel",
            firstname="Michel",
            lastname="Richardo",
            password="michel123456789",
            phone="+221701230738",
            user_type=coach
        )

        self.jasmine = Account.objects.create_user(
            email="jasmine@mail.com",
            username="jasmine",
            firstname="Jasmine",
            lastname="Ndour",
            password="jasmine123456789",
            user_type=client
        )

        self.amina = Account.objects.create_user(
            email="aminata@mail.com",
            username="aminata",
            firstname="aminata",
            lastname="Duboi",
            password="aminata123456789",
            height=173,
            user_type=docteur
        )

        self.doudou = Account.objects.create_user(
            email="doudou@mail.com",
            username="doudou",
            firstname="doudou",
            lastname="ndiaye",
            password="doudou123456789",
            sexe="M",
            user_type=docteur
        )
