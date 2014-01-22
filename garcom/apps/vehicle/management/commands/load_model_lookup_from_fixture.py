# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import StringIO, tarfile, os
from django.conf import settings
from django.core import management


class Command(BaseCommand):
    args = '<No arguments>'
    help = 'This command will load all models lookup from JSON Fixture.'
    _vehicle_database = 'model_lookup.json.tag.gz'

    def handle(self, *args, **options):
        try:
            compressed_file = '%s/garcom/apps/vehicle/fixtures/%s' % (
                getattr(settings, 'BASE_DIR'), self._vehicle_database)

            if not os.path.isfile(compressed_file):
                raise CommandError('%s does not exists in fixture' % self._vehicle_database)


            tar = tarfile.open(mode="r:gz", fileobj = file(compressed_file))

            member = tar.getnames()

            jsonfile = tar.extractfile(member[0]).read()

            management.call_command('loaddata', '%s/garcom/apps/vehicle/fixtures/%s' % (getattr(settings, 'BASE_DIR'), 'model_lookup.json'))





        except  Exception as e:
            raise CommandError('Exception: %s' % str(e))

