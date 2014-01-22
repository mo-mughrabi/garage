from django import http
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import check_for_language
from garcom.apps.accounts.models import Profile

def set_i18n(request, language):
    # TODO: Buggy approach, this must be replaced with django out of the box view (which for some reason did not work with me)
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    next = next.replace('/%s' % request.LANGUAGE_CODE, '')
    response = http.HttpResponseRedirect(next)

    lang_code = language
    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

    # update user profile if user is logged in
    if request.user.is_authenticated():
        Profile.objects.filter(user=request.user).update(preferred_language=lang_code)

    return response


def javascript(request):
    return render_to_response(
        'common/common_js.html',
        {

        },
        RequestContext(request),
        mimetype='application/x-javascript'
    )

def no_javascript(request):
    return render_to_response(
        'common/no_javascript.html',
            {

        },
        RequestContext(request)
    )