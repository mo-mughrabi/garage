# -*- coding: utf-8 -*-
import glob, os
from django.contrib.auth.models import User
from django.core.files.base import File
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from garcom.apps.vehicle.models import Car, ModelLookup, Image, Lookup
from random import choice, randint
from django.utils.translation import activate


class Command(BaseCommand):
    args = '<num_of_cars>'
    help = ''


    def handle(self, *args, **options):
        try:
            # activate english language to print
            # model title in english
            activate('en')

            num_of_cars = int(args[0])

            fixture_folder = '%s/garcom/apps/vehicle/fixtures/' % getattr(settings, 'BASE_DIR')

            os.chdir('%s%s' % (fixture_folder, 'images'))
            files = glob.glob("*")

            user = User.objects.get(id=1)

            for i in range(1, num_of_cars + 1):
                random_model = ModelLookup.objects.order_by('?')[0]
                random_color = Lookup.objects.filter(group='COLOR').order_by('?')[0]

                car = Car(status=Car.STATUS_ACTIVE,
                          description='Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum',
                          mileage=randint(1, 10000),
                          asking_price=randint(1, 100000),
                          condition=u'U',
                          color=random_color,
                          created_by=user, model=random_model,
                )
                car.save()

                for x in range(0, randint(1, len(files))):
                    image = Image(
                        car=car,
                        status=Image.STATUS_ACTIVE,
                        image=File(open(choice(files), 'r')))
                    image.save()

                car.primary_image = image
                car.save()

                print 'car %i added saved..' % i




        except IndexError:
            raise CommandError('must specify number of cars to be created.')
        except  Exception as e:
            raise CommandError('Exception: %s' % str(e))


