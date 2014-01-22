# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('garcom.apps.accounts.views',

                       url(r'^$', 'index',
                           name='accounts-index'),


                       url(r'^login/$', 'login',
                           name='accounts-login'),
                       url(r'^logout/$', 'logout',
                           name='accounts-logout'),
                       url(r'^register/$', 'register',
                           name='accounts-register'),
                       url(r'^activate/(?P<verification_code>[-\w]+)/$',
                           'verify_account', name='accounts-verify'),

                       url(r'^recovery/$', 'recovery',
                           name='accounts-recovery'),
                       url(r'^recovery/(?P<pass_phrase>[-\w]+)/$', 'recovery',
                           name='accounts-recovery-pass-phrase'),


                       url(r'^profile/$', 'profile',
                           name='accounts-profile'),
                       url(r'^profile/general/', 'profile_general',
                           name='accounts-profile-general'),

                       url(r'^profile/payments/$',
                           'profile_payments', name='accounts-profile-payment'),
                       url(
                       r'^profile/payments/make-primary/(?P<make_primary>\d+)/$',
                       'profile_payments', name='accounts-profile-payment-make-primary'),
                       url(
                       r'^profile/payments/delete/(?P<delete_payment>\d+)/$',
                       'profile_payments', name='accounts-profile-del-payment'),

                       url(r'^profile/contacts/$',
                           'profile_contacts', name='accounts-profile-contacts'),
                       url(
                       r'^profile/contacts/make-primary/(?P<make_primary>\d+)/$',
                       'profile_contacts', name='accounts-profile-contact-make-primary'),
                       url(r'^profile/contacts/delete/(?P<delete_phone>\d+)/$',
                           'profile_contacts', name='accounts-profile-contact-delete'),





                       url(r'^profile/my-vehicles/$',
                           'my_vehicle', name='accounts-profile-my-vehicles'),

                       )

urlpatterns += patterns('',
                        url(r'', include('social_auth.urls'))
                        )

urlpatterns += patterns('django.views.generic.simple',
                       (r'^auth-error/$', 'direct_to_template', {'template':
                                                                 'accounts/auth-error.html'}),

                        )
