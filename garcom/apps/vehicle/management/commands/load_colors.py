# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from garcom.apps.vehicle.models import Lookup
from django.conf import settings
import json


class Command(BaseCommand):
    args = ''
    help = ''


    def handle(self, *args, **options):
        try:

            file = '%s/garcom/apps/vehicle/fixtures/colors.json' % (getattr(settings, 'BASE_DIR'))
            data = json.load(open(file))

            user = User.objects.get(id=1)

            for key, color in data.iteritems():

                lookup = Lookup(
                    group='COLOR',
                    key=key,
                    created_by=user
                )
                lookup.translate('en')
                lookup.value = color
                lookup.save()


        except  Exception as e:
            raise CommandError('Exception: %s' % str(e))
