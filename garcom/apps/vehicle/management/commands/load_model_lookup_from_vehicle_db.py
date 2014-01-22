# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import StringIO, csv, tarfile, os
from django.conf import settings
from ...models import ModelLookup, ModelLookUpI18n
from django.db import transaction
from django.template.defaultfilters import slugify


class Command(BaseCommand):
    args = '<No arguments>'
    help = 'This command will load all models lookup from the compressed file.'
    _vehicle_database = 'vehicle_database.tar.gz'

    def handle(self, *args, **options):
        try:
            compressed_file = '%s/garcom/apps/vehicle/fixtures/%s' % (
                getattr(settings, 'BASE_DIR'), self._vehicle_database)

            if not os.path.isfile(compressed_file):
                raise CommandError('%s does not exists in fixture' % self._vehicle_database)

            # Open tarfile
            tar = tarfile.open(mode="r:gz", fileobj=file(compressed_file))

            # list of model objects for build insert
            models_objects = []
            i18n_models_objects = []

            # Iterate over every member
            for member in tar.getnames():
                csvfile = tar.extractfile(member).read()

                with transaction.commit_manually():
                    for idx, row in enumerate(csv.reader(StringIO.StringIO(csvfile), delimiter=',')):
                        if idx == 0: continue # skip the header

                        # exceptions
                        # ----------
                        # duplicate rows in the database
                        if row[0] in ['23773', '45313', ]: continue
                        # slugify will transform '+' and '!' to blank
                        if row[0] in ['45309', '45313', '49158', ]: row[3] = 'Plus'
                        if row[0] in ['45310', '45314', '49159', ]: row[3] = 'Exclaim'
                        # trim is called '=+ Automatic'!!!
                        if row[0] in ['56792', '56794', '56796', ]: continue

                        if idx % 500 == 0:
                            ModelLookup.objects.bulk_create(models_objects)

                            ModelLookUpI18n.objects.bulk_create(i18n_models_objects)
                            transaction.commit()

                            models_objects = []
                            i18n_models_objects = []

                            print 'Commited %d' % idx

                        models_objects.append(
                            ModelLookup(
                                id=row[0],
                                make=slugify(row[1]),
                                model=slugify(row[2]),
                                trim=slugify(row[3]),
                                year=int(row[4]),
                                status='A',
                                body_style=row[5] if row[5] != '' else None,
                                engine_position=row[6] if row[6] != '' else None,
                                engine_cylinders=row[8] if row[8] != '' else None,
                                engine_type=row[9] if row[9] != '' else None,
                                engine_power_ps=row[11] if row[11] != '' else None,
                                engine_power_rpm=row[12] if row[12] != '' else None,
                                engine_torque_nm=row[13] if row[13] != '' else None,
                                engine_torque_rpm=row[14] if row[14] != '' else None,
                                engine_fuel=row[18] if row[18] != '' else None,
                                top_speed_kph=row[19] if row[19] != '' else None,
                                drive=row[21] if row[21] != '' else None,
                                transmission_type=row[22] if row[22] != '' else None,
                                seats=row[23] if row[23] != '' else None,
                                doors=row[24] if row[24] != '' else None,
                                weight=row[25] if row[25] != '' else None,
                            ))

                        i18n_models_objects.append(
                            ModelLookUpI18n(
                                model_id=row[0],
                                language='en',
                                make_display=row[36],
                                model_display=row[2],
                                trim_display=row[3],
                            ))

                        total = idx




                    # commit the remaining
                    transaction.commit()

                    print 'Done. Commited a total of %d objects.' % total






        except  Exception as e:
            raise CommandError('Exception: %s' % str(e))

            
