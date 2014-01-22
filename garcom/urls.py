from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': (
        'garcom.apps',
    ),
}

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^i18n/set_lang/(?P<language>[-\w]+)/$', 'garcom.misc.common_lib.views.set_i18n',
                           name='set-i18n'),
)

urlpatterns += patterns('',

                        url(r'^$', 'apps.vehicle.views.index', name='vehicle-index'),
                        url(r'^common-libs/', include('misc.common_lib.urls')),
                        url(r'^account(s)?/', include('apps.accounts.urls')),


                        url(r'^vehicle(s)?/', include('apps.vehicle.urls')),
                        url(r'^pages/', include('apps.pages.urls')),
                        url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

)

handler404 = 'apps.pages.views.handler404'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
