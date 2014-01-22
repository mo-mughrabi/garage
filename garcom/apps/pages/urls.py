# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('apps.pages.views',
                       url(r'^FAQ/$',
                           'faq_index', name='faq-index'),
                       url(r'^contact-us/$', 'contact_us', name='contact-us'),
                       url(r'^terms/$', 'terms_of_service', name='terms-of-service'),
                       )
