from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site


attrs_dict = {'class': 'required span6', }


class ContactForm(forms.Form):

    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs=dict(
                                                  attrs_dict)),
                           label=u'Your name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=200)),
                             label=u'Your email address')
    body = forms.CharField(
        widget=forms.Textarea(
            attrs=dict(attrs_dict)),
        label=u'Your message')

    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

