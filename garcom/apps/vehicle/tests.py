# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
import unittest
from models import Car, ModelLookup


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            model           =   ModelLookup.objects.order_by('?')[0],
            created_by      =   User.objects.get(pk=1),
            asking_price    =   11010
        )
