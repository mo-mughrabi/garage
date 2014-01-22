# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import FaqCategory, Faq
from forms import ContactForm


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            body = 'from {0}\n via {1}\n\n\n message:\n{2}'.format(
                cleaned_data.get('name'),
                cleaned_data.get('email'),
                cleaned_data.get('body'),
            )

            msg = EmailMultiAlternatives('Query from %s Garage' % cleaned_data.get('name'),
                                         body, getattr(settings, 'OUTGOING_EMAILS'),
                                         [mail_tuple[1] for mail_tuple in settings.MANAGERS])
            msg.send()
            return render_to_response(
                'pages/contact-us.html',
                {
                    'form': None,
                },
                context_instance=RequestContext(request)
            )

    else:
        form = ContactForm()
    return render_to_response(
        'pages/contact-us.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def faq_index(request):
    return render_to_response(
        'pages/faq/index.html',
        {
            'faqs': Faq.objects.filter(is_active=True),
            'categories': FaqCategory.objects.filter(is_active=True),
        },
        context_instance=RequestContext(request)
    )


def terms_of_service(request):
    return render_to_response(
        'pages/terms.html',
        {},
        context_instance=RequestContext(request)
    )


def handler404(request):
    """
    """
    return render_to_response(
        'pages/404.html',
        {
            'STATIC_URL': getattr(settings, 'STATIC_URL')
        },
        context_instance=RequestContext(request)
    )
