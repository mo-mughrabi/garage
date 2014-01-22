from django.http import HttpResponseRedirect


def anonymous_required(function=None, home_url=None, redirect_field_name=None):
    """
    """

    if home_url is None:
        # TODO: must allow reverse URL's for the home_url, for now its throwing an exception when associated with reverse URL
        home_url = '/'

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
                url = None
                if redirect_field_name and redirect_field_name in request.REQUEST:
                    url = request.REQUEST[redirect_field_name]
                if not url:
                    url = home_url
                if not url:
                    url = "/"
                return HttpResponseRedirect(url)
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__  = view_func.__name__
        _view.__dict__  = view_func.__dict__
        _view.__doc__   = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)