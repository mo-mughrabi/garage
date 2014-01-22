# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('accounts/inclusions/admin_drop_down.html', takes_context=True)
def get_admin_drop_down(context, user, url):

    return {
        'user': user,
        'url_path': url,
    }


@register.inclusion_tag('accounts/inclusions/user_drop_down.html', takes_context=True)
def get_user_drop_down(context, user, url):

    return {
        'user': user,
        'url_path': url,
    }


@register.inclusion_tag('accounts/inclusions/user_sidebar.html', takes_context=True)
def get_user_sidebar(context, user, url):

    return {
        'user': user,
        'url_path': url,
    }
