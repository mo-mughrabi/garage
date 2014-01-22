# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models.aggregates import Count
from garcom.apps.vehicle.models import ModelLookUpI18n
import urllib2, json
import threading


class TranslatorThread(threading.Thread):
    def __init__(self, queryset, settings, field_name):
        threading.Thread.__init__(self)
        self.queryset = queryset
        self.settings = settings
        self.field_name = field_name


    def run(self):
            for language_code, language in getattr(self.settings, 'LANGUAGES'):
                if language_code in (getattr(self.settings, 'LANGUAGE_CODE'),): break

                for record in self.queryset:
                    kwargs = {
                        '{0}'.format(self.field_name): record[self.field_name]
                    }
                    translated_field = record[self.field_name]#self.translate(record[self.field_name], 'en', language_code)

                    for queryset in ModelLookUpI18n.objects.filter(**kwargs).filter(language='en'):
                        try:

                            f = ModelLookUpI18n.objects.get(model=queryset.model, language='ar')
                            setattr(f, self.field_name, translated_field)
                            f.save()

                        except ModelLookUpI18n.DoesNotExist as e:
                            kwargs = {
                                '{0}'.format(self.field_name): translated_field,
                                'language'                   : language_code,
                                'model_id'                  : queryset.model_id
                            }
                            ModelLookUpI18n(**kwargs).save()




    def translate(self, text, source, target):
        api_key = 'AIzaSyA2TziP368Idl0WgoIkA7Blki3VDBF9LhY'

        text = urllib2.quote(text. encode('utf8'))

        data = urllib2.urlopen('https://www.googleapis.com/language/translate/v2?key=' + api_key + '&source=' + source + '&target=' + target + '&q=' + text).read()

        json_data = json.loads(data)

        return json_data['data']['translations'][0]['translatedText']



class Command(BaseCommand):
    args = '<threads field_name>'
    help = ''


    def handle(self, *args, **options):
        try:

            num_threads = 10
            threads = []
            field_name = 'trim_display'

            if not ModelLookUpI18n._meta.get_field_by_name(field_name):
                print
                exit()

            queryset = ModelLookUpI18n.objects.filter(language='en').values(field_name).annotate(Count(field_name))

            queryset_paginated = Paginator(queryset, queryset.count()/num_threads)

            for i in range(1, num_threads+2):
                queryset_batch = queryset_paginated.page(i)
                t = TranslatorThread(queryset=queryset_batch.object_list, settings=settings, field_name=field_name)
                threads.append(t)
                t.start()


        except  Exception as e:
            raise CommandError('Exception: %s' % str(e))
