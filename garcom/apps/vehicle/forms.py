# -*- coding: utf-8 -*-
from captcha.fields import ReCaptchaField
from django import forms
from django.db.models.aggregates import Count, Max
from garcom.misc.common_lib.forms import ExtendedMetaModelForm
from models import (ModelLookUpI18n as ModelLookup,
                    ModelLookup as ModelLookUpBase, Car, Image)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _, get_language
from widgets import ModelLookupWidget
import logging


logging.getLogger(__name__)


class ModelLookUpForm(ExtendedMetaModelForm):
    '''
    ModelLookUpForm

    '''

    class Meta:
        model = ModelLookUpBase
        fields = (
            'year',
            'body_style',
            'transmission_type',
            'engine_position',
            'engine_cylinders',
            'engine_type',
            'engine_fuel',
            'drive',
            'seats',
            'doors',
            'weight',
            'engine_power_ps',
            'engine_power_rpm',
            'engine_torque_rpm',
        )
        widgets = {
            'year': forms.Select(attrs={'class': 'input-xlarge span5 required', 'required': ''}),
            'body_style': forms.Select(attrs={'class': 'input'}),
            'transmission_type': forms.Select(attrs={'class': 'input'}),
            'engine_position': forms.Select(attrs={'class': 'input'}),
            'engine_cylinders': forms.Select(attrs={'class': 'input'}),
            'engine_type': forms.Select(attrs={'class': 'input'}),
            'engine_fuel': forms.Select(attrs={'class': 'input'}),
            'drive': forms.Select(attrs={'class': 'input'}),
            'seats': forms.Select(attrs={'class': 'input'}),
            'doors': forms.Select(attrs={'class': 'input'}),
            'weight': forms.TextInput(attrs={'class': 'input'}),
            'engine_power_ps': forms.TextInput(attrs={'class': 'input'}),
            'engine_power_rpm': forms.TextInput(attrs={'class': 'input'}),
            'engine_torque_rpm': forms.TextInput(attrs={'class': 'input'}),
        }
        field_args = {
            'year': {
                'required_field': True,
            },
        }

    def __init__(self, *args, **kwargs):
        super(ModelLookUpForm, self).__init__(*args, **kwargs)

        # TODO: must translate body_type in i18n Table
        self.fields['body_style'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values(
            'body_style', 'body_style').annotate(Count('body_style')).values_list('body_style', 'body_style')
        self.fields['engine_position'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values(
            'engine_position', 'engine_position').annotate(Count('engine_position')).values_list('engine_position',
                                                                                                 'engine_position')
        self.fields['engine_cylinders'].widget.choices = self.Meta.model.objects.filter(
            body_style__isnull=False).values('engine_cylinders', 'engine_cylinders').annotate(
            Count('engine_cylinders')).values_list('engine_cylinders', 'engine_cylinders')
        self.fields['engine_type'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values(
            'engine_type', 'engine_type').annotate(Count('engine_type')).values_list('engine_type', 'engine_type')

        self.fields['engine_fuel'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values(
            'engine_fuel', 'engine_fuel').annotate(Count('engine_fuel')).values_list('engine_fuel', 'engine_fuel')
        self.fields['drive'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values('drive',
                                                                                                              'drive').annotate(
            Count('drive')).values_list('drive', 'drive')
        self.fields['transmission_type'].widget.choices = self.Meta.model.objects.filter(
            body_style__isnull=False).values('transmission_type', 'transmission_type').annotate(
            Count('transmission_type')).values_list('transmission_type', 'transmission_type')
        self.fields['doors'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values('doors',
                                                                                                              'doors').annotate(
            Count('doors')).values_list('doors', 'doors')
        self.fields['weight'].widget.choices = self.Meta.model.objects.filter(body_style__isnull=False).values('weight',
                                                                                                               'weight').annotate(
            Count('weight')).values_list('weight', 'weight')

        # append ng-model for each field for angularJS
        for field in self.fields:
            self.fields[field].widget.attrs['ng-model'] = 'data.%s' % field

    def all_optional_fields(self):
        return [field for field in self if not field.is_hidden and getattr(field.field, 'required_field', None) is None]

    def all_required_fields(self):
        return [field for field in self if not field.is_hidden and getattr(field.field, 'required_field', None) == True]


class ModelLookUpI18nForm(ExtendedMetaModelForm):
    '''
    ModelLookUpI18nForm
    '''

    class Meta:
        model = ModelLookup  # ModelLookup is referenced to ModelLookupI18n
        fields = ('make_display', 'model_display', 'trim_display')

        widgets = {
            'make_display': forms.TextInput(
                {'placeholder': _('Car make e.g (Mercedes Benz, Dodge)'), 'class': 'input-xlarge span5 required',
                 'required': ''}),
            'model_display': forms.TextInput(
                {'placeholder': _('Car model e.g (E, Charger)'), 'class': 'input-xlarge span5 required',
                 'required': ''}),
            'trim_display': forms.TextInput(
                {'placeholder': _('Car trim e.g (350 Coupe, R/T)'), 'class': 'input-xlarge span5 required'}),
        }

    def __init__(self, *args, **kwargs):
        super(ModelLookUpI18nForm, self).__init__(*args, **kwargs)
        self.fields['make_display'].label = _('Car Make')
        self.fields['model_display'].label = _('Model Make')
        self.fields['trim_display'].label = _('Trim Make')

        for field in self.fields:
            self.fields[field].widget.attrs['ng-model'] = 'data.%s' % field


class CarForm(ExtendedMetaModelForm):
    """
    CarForm

    """

    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={'multiple': ''}))

    class Meta:
        model = Car
        fields = ('model', 'description', 'condition', 'mileage',
                  'asking_price', 'color', 'primary_image', 'status', 'contact_phone')
        widgets = {
            'mileage': forms.TextInput(
                attrs={'placeholder': _('Approximate mileage'), 'class': 'step2 input-large ', 'ng-model': 'mileage',
                       'required': ''}),
            'asking_price': forms.TextInput(
                attrs={'placeholder': _('Asking price'), 'class': 'step2 input-large ', 'ng-model': 'price', }),
            'description': forms.Textarea(
                attrs={'placeholder': _('Your description should not exceed 200 words.'), 'class': 'step2 input-xlarge',
                       'rows': '5', 'ng-model': 'description'}),
            'color': forms.Select(
                attrs={
                    'class': 'step2 input-xlarge',
                    'ng-model': 'color',
                    'ng-options': 'color.id as color.value for color in colors',
                    'required': ''
                }
            ),
            'condition': forms.Select(
                attrs={
                    'class': 'step2 input-xlarge',
                    'ng-model': 'condition',
                    'required': _('Condition is required.')
                }
            ),
            'primary_image': forms.HiddenInput(attrs={'ng-model': 'primaryimage', 'required': ''}),
            # 'contact_email': forms.TextInput(attrs={'ng-model': 'email', 'data-provide': 'typeahead'}),
            'contact_phone': forms.TextInput(attrs={'ng-model': 'phone', 'data-provide': 'typeahead'})
        }
        field_args = {
            'model': {
                'error_messages': {
                    'required': _('Model selection is required.')
                },
                'column': 'left',
                'label': '',
            },
            'mileage': {
                'error_messages': {
                    'required': _('Mileage is required.'),
                    'invalid': _('Mileage must be a number/decimal')
                },
                'column': 'center'
            },
            'color': {
                'error_messages': {
                    'required': _('Color is required.')
                },
                'column': 'center'
            },
            'condition': {
                'error_messages': {
                    'required': _('Condition is required.')
                },
                'column': 'center'
            },
            'asking_price': {
                'error_messages': {
                    'required': _('Price is required.'),
                    'invalid': _('Price must be number/decimal')
                },
                'column': 'center'
            },
            'description': {
                'error_messages': {
                    'required': _('Price is required.'),
                },
                'column': 'center'
            },
            'primary_image': {
                'error_messages': {
                    'required': _('Cover image must be selected.'),
                },
                'column': 'right'
            },
            'contact_email': {
                'label': 'Email',
            },
            'contact_phone': {
                'label': 'Phone'
            },
        }

    def __init__(self, *args, **kwargs):
        try:
            self.user = kwargs.get('user', None)
            kwargs.pop('user', None)

            super(CarForm, self).__init__(*args, **kwargs)

            if not self.user:
                raise
            self.fields['color'].choices = [('', _('Select a color')), ]
            self.fields['contact_email'].widget.attrs['data-source'] = '["%s"]' % self.user.email
            self.fields['contact_phone'].widget.attrs['data-source'] = str(
                ["%d" % int(phone.number) for phone in self.user.profile.phone_set.all()]).replace('\'', '"')

        except Exception as e:
            self.fields['color'].choices = [('', _('Select a color')), ]
            self.fields['asking_price'].required = False
            self.fields['model'].widget = ModelLookupWidget(user=self.user)






    def left_column(self):
        return [field for field in self if not field.is_hidden and getattr(field.field, 'column', None) == 'left']

    def center_column(self):
        return [field for field in self if not field.is_hidden and getattr(field.field, 'column', None) == 'center']

    def right_column(self):
        return [field for field in self if not field.is_hidden and getattr(field.field, 'column', None) == 'right']

    def clean(self):
        cleaned_data = super(CarForm, self).clean()

        # override form validation for Draft
        if cleaned_data.get('status') == Car.STATUS_DRAFT:
            self._errors.clear()

        # make sure either email or phone are set
        if cleaned_data.get('contact_email') == '' and cleaned_data.get('contact_phone') == '':
            return forms.ValidationError('At least one contact must be set.')

        return cleaned_data


class ImageInlineForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Image
        widgets = {
            'image': forms.FileInput(),
        }


class CarAdminForm(forms.ModelForm):
    """
    Used to render admin site form for Car
    """

    def __init__(self, *args, **kwargs):

        super(CarAdminForm, self).__init__(*args, **kwargs)
        try:
            # TODO: Implement multiple select widget for model look up for
            # performance
            self.fields['model'].queryset = ModelLookup.objects.filter(
                make=self.instance.model.make).order_by('model__year')
            self.fields['primary_image'].queryset = Image.objects.filter(
                car=self.instance.id)
        except ObjectDoesNotExist:
            self.fields['model'].queryset = ModelLookup.objects.order_by(
                'model__year')
            self.fields['primary_image'].queryset = Image.objects.get_empty_query_set()
