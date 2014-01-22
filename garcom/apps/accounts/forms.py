# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.template.defaultfilters import safe
from django.utils.translation import ugettext_lazy as _
from garcom.misc.common_lib.forms import ExtendedMetaModelForm
from models import Profile, Phone, Payment, PasswordRecovery
from datetime import datetime
from django.forms import extras


class LoginForm(forms.Form):
    """
    LoginForm:

    """
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'required': ''}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': ''}))
    next = forms.CharField(widget=forms.HiddenInput())


class UserForm(ModelForm):
    """
    UserForm:

    """
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', )




class PhoneInlineForm(ExtendedMetaModelForm):
    class Meta:
        model = Phone
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }
        field_args = {
            'type': {
                'error_messages': {
                    'required': _('Contact type is required.')
                }
            },
        }

    def clean(self):
        cleaned_data = super(PhoneInlineForm, self).clean()
        try:
            int(cleaned_data.get('number'))
        except ValueError, TypeError:
            self._errors['number'] = self.error_class(
                [_('Number must consist of numbers only.')])
            del cleaned_data['number']

        return cleaned_data


class PaymentInlineForm(ModelForm):
    class Meta:

        model = Payment
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Card Number'}),
        }


class RegistrationForm(ExtendedMetaModelForm):
    _genders = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    birthday = forms.DateField(
        widget=extras.SelectDateWidget(attrs={'class': 'span1'}, years=(
            range(1930, datetime.now().year - 14))),
        label = _('Birthday'),
        required= True,
        error_messages = {
            'required': _('Birthday is required.')
        }

    )
    gender = forms.CharField(
        label=_('Gender'),
        widget=forms.Select(choices=_genders)
    )

    password_confirm = forms.CharField(
        label=_('Password (again)'),
        required=True,
        error_messages={
            'required': _('Password confirmation is required.')
        },
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Password confirmation')})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'gender',
                  'email', 'password', 'password_confirm')

        widgets = {
            'password': forms.PasswordInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.TextInput(),
        }
        field_args = {
            'first_name': {
                'error_messages': {
                    'required': _('First name is required')
                }
            },
            'last_name': {
                'error_messages': {
                    'required': _('Last name is required')
                }
            },
            'email': {
                'error_messages': {
                    'required': _('Email address is required')
                }
            },
        }

    def __init__(self, *args, **kwargs):

        super(RegistrationForm, self).__init__(*args, **kwargs)

        # required fields to over-ride model
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        for i in self.fields:
            if isinstance(self.fields[i], forms.CharField):
                self.fields[i].widget.attrs["class"] = 'input-xlarge'

    def required_fields(self):
        return [field for field in self if not field.is_hidden and field.name in self.Meta.fields]

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        # validate if email exists in our database
        try:
            User.objects.get(email=cleaned_data.get('email', None))
            self._errors['email'] = self.error_class([_(safe('Your email already exists in our system. If you do not remember your password try our recovery <a href="%s">here</a>. ' % reverse('accounts-login')))])
            del cleaned_data['email']
        except User.DoesNotExist:
            pass

        # validate if passwords are matching & not less than 8 characters
        try:

            if cleaned_data.get('password', None) != cleaned_data.get('password_confirm', None):
                self._errors['password'] = self.error_class(
                    [_('Password does not match.')])
                del cleaned_data['password']

            elif len(cleaned_data.get('password', '')) < getattr(settings, 'GARAGE_PASSWORD_LENGTH', 8):
                self._errors['password'] = self.error_class(
                    [_('Password cannot be less than 8 characters.')])
                del cleaned_data['password']

        except KeyError as e:
            self._errors['password'] = self.error_class(
                [_('Password error cannot be blank.')])

        return cleaned_data


class RecoveryForm(forms.Form):
    """
        form used to reset user password via email address
    """

    email = forms.CharField(
        label       =_('email'),
        widget      =forms.TextInput(attrs={'placeholder': _('Your email address')}),
        required    =True
    )

    def clean(self):
        cleaned_data = super(RecoveryForm, self).clean()

#        if cleaned_data.get('email', None) is None:
#            self._errors['email'] = self.error_class([_(
#                'Email does not exists.')])


        # validate if email exists in our database
        try:
            User.objects.get(email=cleaned_data.get('email', None))
        except User.DoesNotExist:
            self._errors['email'] = self.error_class([_(
                'Email does not exists.')])
            if hasattr(cleaned_data, 'email'):
                del cleaned_data['email']

        # validate if a pass phrase is created in our password recovery table
        try:
            PasswordRecovery.objects.get(
                user=User.objects.get(
                    email=cleaned_data.get('email', None)),
                expires_at__gte=datetime.now(),
            )
            self._errors['email'] = self.error_class(
                [_('A reset link has been resent to your mail box.')])
            if hasattr(cleaned_data, 'email'):
                del cleaned_data['email']
        except PasswordRecovery.DoesNotExist:
            pass
        except PasswordRecovery.MultipleObjectsReturned:
            pass
        except User.DoesNotExist:
            pass

        return cleaned_data
