from django.conf.urls import *

urlpatterns = patterns('garcom.misc.common_lib.views',
    url(r'^common_js.js$',             'javascript',                name='common-lib-javascript'),
    url(r'^nojscript.html$',           'no_javascript',             name='common-lib-no_javascript'),
)
