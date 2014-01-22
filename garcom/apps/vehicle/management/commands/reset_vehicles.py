# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from garcom.apps.vehicle.models import Car, ModelLookup, Image



class Command(BaseCommand):
    args = ''
    help = ''


    def handle(self, *args, **options):
        try:


            cars = Car.objects.all()
            cars.delete()
            images = Image.objects.all()
            images.delete()


        except  Exception as e:
            raise CommandError('Exception: %s' % str(e))
