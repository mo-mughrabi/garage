# -*- coding: utf-8 -*-
from django.forms.widgets import MultiWidget, Select, HiddenInput
from django.utils.safestring import mark_safe
from models import ModelLookUpI18n as ModelLookup
from django.utils.translation import ugettext as _, get_language
import logging

logger = logging.getLogger(__name__)


class ModelLookupWidget(MultiWidget):

    def __init__(self, user, attrs=None):
        self.user = user

        widgets = (
            Select(
                choices=[('', _('Select an option')), ],
                attrs={'class': 'model-make input-xlarge',
                       'ng-model': 'make',
                       'ng-options': 'make.make as make.display for make in makes',
                       'ng-change': ''}
            ),  # make
            Select(
                choices=[('', _('Select an option')), ],
                attrs={'class': 'model-year input-xlarge',
                       'ng-model': 'year',
                       'ng-options': 'year as year for year in years',
                       'ng-disabled': '!make || !years.length',
                       'ng-change': ''},
            ),  # year
            Select(
                choices=[('', _('Select an option')), ],
                attrs={'class': 'model-model input-xlarge',
                       'ng-model': 'model',
                       'ng-options': 'model.model as model.display for model in models',
                       'ng-disabled': '!year || !models.length',
                       'ng-change': ''}
            ),  # model
            Select(
                choices=[('', _('Select an option')), ],
                attrs={'class': 'model-trim input-xlarge',
                       'ng-model': 'trim',
                       'ng-options': 'trim.trim as trim.display for trim in trims',
                       'ng-disabled': '!model || !trims.length',
                       'ng-change': ''}),  # trim
            HiddenInput(attrs={'ng-model': 'modelkey', 'required': ''})
        )

        super(ModelLookupWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        # debugging widget returned value
        #logging.debug('value_from_datadict: ' % [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)])

        return [widget.value_from_datadict(data, files, name + '_%d' % i) for i, widget in enumerate(self.widgets)][4]

    def decompress(self, value):
        if value:
            self.value_list = ModelLookup.objects.values_list('model__make', 'model__year', 'model__model', 'model__trim', 'model__id').get(model__id=value, language=get_language())
            # self.populate_select(self.value_list, value)
            return self.value_list

        return [None, None, None, None, None]

    def populate_select(self, value_list, model_id):

        self.widgets[1].choices = ModelLookup.objects.distinct_years(make=value_list[0]).values_list('model__year', 'model__year').order_by('-model__year')
        self.widgets[2].choices = ModelLookup.objects.distinct_model(make=value_list[0], year=value_list[1]).values_list('model__model', 'model_display').order_by('model__model', 'model__year')
        self.widgets[3].choices = ModelLookup.objects.distinct_trim(make=value_list[0], model=value_list[2], year=value_list[1]).values_list('model__trim', 'trim_display').order_by('model__trim')

    def render(self, name, value, attrs=None):
        # HTML to be added to the output
        widget_labels = [
            '<label for="id_%(label_id)s">%(label)s </label>' % {
                'label_id': '%(label_id)s',
                'label': _('Make')
            },
            '<label for="id_%(label_id)s">%(label)s </label>' % {
                'label_id': '%(label_id)s',
                'label': _('Year')
            },
            '<label for="id_%(label_id)s">%(label)s </label>' % {
                'label_id': '%(label_id)s',
                'label': _('Model')
            },
            '<label for="id_%(label_id)s">%(label)s </label>' % {
                'label_id': '%(label_id)s',
                'label': _('Trim')
            },
            '<label for="id_%(label_id)s"></label>' % {
                'label_id': '%(label_id)s',
            }
        ]

        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        # value is a list of values, each corresponding to a widget in
        # self.widgets

        if not isinstance(value, list):
            value = self.decompress(value)

        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None

            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))

            output.append(
                widget_labels[i] % {'label_id': '%s_%s' % (name, i)})

            output.append(
                widget.render(name + '_%s' % i, widget_value, final_attrs))

        return mark_safe(self.format_output(output))
