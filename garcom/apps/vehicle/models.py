# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.timesince import timesince
import tasks
import logging
import uuid
import datetime
from django.utils.translation import ugettext as _, get_language
from hvad.models import TranslatableModel, TranslatedFields
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail, delete

# initiate logger
logging.getLogger(__name__)


class ModelLookUpManager(models.Manager):
    pass


class ModelLookup(models.Model):
    # generate years from 1930 until next year
    _years = map(
        lambda x: (x, x), range(1930, datetime.datetime.now().year + 2))
    STATUS_APPROVED = 'A'
    STATUS_SUGGESTED = 'S'
    STATUS_REJECTED = 'R'
    _statuses = (
        (STATUS_APPROVED, _('Active')),
        (STATUS_SUGGESTED, _('Suggested')),
        (STATUS_REJECTED, _('Rejected')),
    )
    _default_status = 'S'

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    trim = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(choices=_years)

    status = models.CharField(max_length=1, choices=_statuses,
                              default=_default_status, db_index=True)
    body_style = models.CharField(max_length=32, null=True, blank=True)
    engine_position = models.CharField(max_length=32, null=True, blank=True)
    engine_cylinders = models.CharField(max_length=32, null=True, blank=True)
    engine_type = models.CharField(max_length=32, null=True, blank=True)
    engine_power_ps = models.CharField(max_length=32, null=True, blank=True)
    engine_power_rpm = models.CharField(max_length=32, null=True, blank=True)
    engine_torque_nm = models.CharField(max_length=32, null=True, blank=True)
    engine_torque_rpm = models.CharField(max_length=32, null=True, blank=True)
    engine_fuel = models.CharField(max_length=32, null=True, blank=True)
    top_speed_kph = models.CharField(max_length=32, null=True, blank=True)
    drive = models.CharField(max_length=32, null=True, blank=True)
    transmission_type = models.CharField(max_length=32, null=True, blank=True)
    seats = models.CharField(max_length=32, null=True, blank=True)
    doors = models.CharField(max_length=32, null=True, blank=True)
    weight = models.CharField(max_length=32, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_create", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_update")
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_approve")

    objects = ModelLookUpManager()

    class Meta:
        unique_together = ('make', 'model', 'trim', 'year',)

    def __unicode__(self):
        return u'%d %s %s' % (self.year, self.model, self.make)

    def get_status(self):
        return self.status

    def save(self, force_insert=False, force_update=False, using=None):
        if self.status == 'S':
            if self.make in ('', u'', None):
                self.make = str(uuid.uuid4())
            if self.model in ('', u'', None):
                self.model = str(uuid.uuid4())
            if self.trim in ('', u'', None):
                self.trim = str(uuid.uuid4())

        super(ModelLookup, self).save(force_insert=False,
                                      force_update=False, using=None)


class ModelLookUpI18nManager(models.Manager):

    def distinct_make(self, user=None, exist=False):
        """
            To retrieve a unique value of makes its faster to use annotate because it will perform
            a count(make) grouped by make whereby make is unique. While the distinct function, is returning
            a full raw distinct and using internal python functionality to filter for distinct make
        """
        try:
            qs = super(ModelLookUpI18nManager, self).get_query_set()

            qs = qs.filter(language=get_language())
            qs = qs.filter(Q(Q(model__created_by=user) & Q(model__status='S')) | Q(model__created_by__isnull=True) & Q(model__status='A'))
            if exist:
                qs = qs.filter(model__in=Car.objects.filter(
                    status=Car.STATUS_ACTIVE).values('model').distinct())

            return qs.values('model__make', 'make_display').annotate(Count('model__make')).order_by('model__make')

        except Exception as e:
            logging.error(str(e))

    def distinct_model(self, make=None, year=None, exist=False):
        try:
            qs = super(ModelLookUpI18nManager, self).get_query_set()

            if exist:
                qs = qs.filter(model__in=Car.objects.filter(
                    status=Car.STATUS_ACTIVE).values('model').distinct())

            if make is None and year is None:
                qs = qs.filter(language=get_language()).\
                    values('model__model', 'model_display').\
                    annotate(Count('model__model'))
            elif make is None:
                qs = qs.filter(model__year=year, language=get_language()).\
                    values('model__model', 'model_display').\
                    annotate(Count('model__model'))
            elif year is None:
                qs = qs.filter(model__make=make, language=get_language()).\
                    values('model__model', 'model_display').\
                    annotate(Count('model__model'))
            else:
                qs = qs.filter(model__year=year, model__make=make, language=get_language()).\
                    values('model__model', 'model_display').\
                    annotate(Count('model__model'))

            return qs

        except Exception as e:
            logging.error(str(e))

    def distinct_trim(self, make=None, model=None, year=None, exist=False):
        try:
            qs = super(ModelLookUpI18nManager, self).get_query_set()

            if exist:
                qs = qs.filter(model__in=Car.objects.filter(
                    status=Car.STATUS_ACTIVE).values('model').distinct())

            if make is None and model is None and year is None:
                qs = qs.filter(language=get_language()).\
                    values('model__trim', 'trim_display').\
                    annotate(Count('model__trim'))
            elif make and model and year is None:
                qs = qs.filter(language=get_language(), model__make=make, model__model=model).\
                    exclude(model__trim__exact='').\
                    values('model__trim', 'trim_display').\
                    annotate(Count('model__trim'))
            else:
                qs = qs.filter(language=get_language(), model__make=make, model__model=model, model__year=year).\
                    exclude(model__trim__exact='').\
                    values('model__trim', 'trim_display').\
                    annotate(Count('model__trim'))

            return qs

        except Exception as e:
            logging.error(str(e))

    def distinct_years(self, make=None, model=None, trim=None, exist=False):
        try:
            qs = super(ModelLookUpI18nManager, self).get_query_set()
            qs.filter(language=get_language())

            if exist:
                qs = qs.filter(model__in=Car.objects.filter(
                    status=Car.STATUS_ACTIVE).values('model').distinct())

            if make is None and model is None and trim is None:
                qs = qs.values('model__year').\
                    annotate(Count('model__year'))
            elif model is None and trim is None:
                qs = qs.filter(model__make=make).\
                    values('model__year').\
                    annotate(Count('model__year'))
            elif trim is None:
                qs = qs.filter(model__make=make, model__model=model).\
                    values('model__year').\
                    annotate(Count('model__year'))
            else:
                qs = qs.filter(model__make=make, model__model=model, model__trim=trim).\
                    values('model__year').\
                    annotate(Count('model__year'))

            return qs
        except Exception as e:
            logging.error(str(e))


class ModelLookUpI18n(models.Model):
    model = models.ForeignKey(ModelLookup)
    language = models.CharField(max_length=5, default=getattr(settings, 'LANGUAGE_CODE', 'en'), choices=getattr(settings, 'LANGUAGES'))

    make_display = models.CharField(max_length=100,)
    model_display = models.CharField(max_length=100)
    trim_display = models.CharField(max_length=100, blank=True, null=True)

    objects = ModelLookUpI18nManager()

    class Meta:
        db_table = 'vehicle_modellookup_i18n'
        unique_together = ('model', 'language')

    def __unicode__(self):
        return u'%s %s %s' % (self.make_display, self.model_display, self.trim_display)


class Lookup(TranslatableModel):
    _group_choices = (
        ('COLOR', _('Color')),
    )
    group = models.CharField(max_length=30, choices=_group_choices)
    key = models.CharField(max_length=30, db_index=True)

    created_by = models.ForeignKey(User, )
    created_at = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        value=models.CharField(
            max_length=200, help_text=_('lookup value')),
    )

    class Meta:
        unique_together = ('key', 'group')

    def __unicode__(self):
        return u'%s' % self.value


class CarManager(models.Manager):
    """
    """

    def get_query_set(self):
        two_months_ago = datetime.datetime.now() - relativedelta(months=-2)
        return super(CarManager, self).get_query_set().exclude(status=self.model.STATUS_SOLD, sold_at__lt=two_months_ago)

    def published_cars(self):
        return self.filter(status='A', for_sale=True).order_by('-created_at')

    def my_cars(self, user):
        return self.filter(created_by=user)


class Car(models.Model):
    STATUS_ACTIVE = 'A'
    STATUS_SOLD = 'S'
    STATUS_PENDING = 'P'
    STATUS_REJECTED = 'R'
    STATUS_DRAFT = 'D'

    _statuses = (
        (STATUS_SOLD, _('Sold')),
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_DRAFT, _('Draft')),
    )
    _default_status = 'D'

    CONDITIONS = (
        (u'N', _('New')),
        (u'U', _('Used')),
    )
    _default_condition = 'N'

    model = models.ForeignKey(ModelLookup, )
    status = models.CharField(max_length=1, choices=_statuses, default=_default_status)
    description = models.TextField(null=True, blank=True)
    primary_image = models.OneToOneField('Image', related_name='is_primary', null=True, blank=True, )
    color = models.ForeignKey('Lookup', limit_choices_to={'group': 'Color'}, null=True, blank=True)
    mileage = models.IntegerField(_('Mileage'), default=0)
    condition = models.CharField(max_length=30, choices=CONDITIONS, default=_default_condition)
    contact_phone = models.CharField(max_length=128, default='')

    for_sale = models.BooleanField(default=True)

    view_count = models.BigIntegerField(default=0)

    asking_price = models.DecimalField(
        _('Price'), max_digits=12, decimal_places=3, blank=True, null=True)
    sold_price = models.DecimalField(_(
        'Sold price'), max_digits=12, decimal_places=3, null=True, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_create")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_update")

    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_approve")

    objects = CarManager()

    def __unicode__(self):
        # print self
        return u'%s' % self.model

    @property
    def _get_model_display(self):
        """ will return QuerySet"""
        try:
            return self.model.modellookupi18n_set.values('make_display', 'model_display', 'trim_display').get(language=get_language())
        except :
            pass

    def get_model_display(self):
        """will return single string"""
        return '%s %s %s' % self.model.modellookupi18n_set.values_list('make_display', 'model_display', 'trim_display').get(language=get_language())

    def available_i18n_models(self):
        return self.model.modellookupi18n_set.count()

    @models.permalink
    def get_absolute_url(self):
        return (
            'vehicle-profile', (), {
                'year': self.model.year,
                'make': self.model.make,
                'model': self.model.model,
                'hex_id': '%05X' % self.id
            }
        )

    def created_since(self):
        return timesince(self.created_at)

    def created_at_format(self):
        return self.created_at.strftime('%d %b %Y %H:%M')

    def status_label(self):
        return dict(self._statuses)[self.status]

    def thumbnail(self):
        try:
            return self.primary_image.thumbnail
        except Exception as e:
            return ''

    def created_by_username(self):
        return self.created_by.username

    def save(self, force_insert=False, force_update=False, using=None):
        super(Car, self).save(
            force_insert=force_insert, force_update=force_update, using=using)


class Image(models.Model):
    STATUS_ACTIVE = 'A'
    STATUS_REJECTED = 'R'
    STATUS_DRAFT = 'D'

    _statuses = (
        (STATUS_ACTIVE, _('Active')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_DRAFT, _('Draft')),
    )

    car = models.ForeignKey(Car, null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=_statuses, default=STATUS_DRAFT)
    image = ImageField(upload_to='cars/full')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_create", null=True, blank=True)

    @property
    def is_primary(self):
        return car.primary_image == self

    @property
    def thumbnail(self):
        thumbnail = get_thumbnail(self.image, '200x128', crop='center', quality=99)
        return '{0}{1}'.format(getattr(settings, 'MEDIA_URL'), thumbnail.name)

    def thumbnail_by_size(self, h, w):
        thumbnail = get_thumbnail(self.image, '{0}x{1}'.format(h,w), quality=100)
        return '{0}{1}'.format(getattr(settings, 'MEDIA_URL'), thumbnail.name)

    def save(self, *args, **kwargs):
        flag = None
        if not self.pk:
            flag = True
        super(Image, self).save(*args, **kwargs)
        if flag:
            tasks.add_watermark.delay(self.pk)



@receiver(pre_delete, sender=Image, dispatch_uid='vehicle.delete_thumbnail')
def delete_thumbnail(sender, instance, using, **kwargs):
    f = instance.image
    delete(f, delete_file=True)
