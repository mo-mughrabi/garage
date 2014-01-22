# -*- coding: utf-8 -*-
from hvad.models import TranslatableModel, TranslatedFields
from django.db import models
from django.utils.timezone import utc
from datetime import datetime
import uuid
from django.utils.translation import ugettext_lazy as _


class Content(TranslatableModel):
    """
    """
    slug = models.CharField(max_length=250, default=str(uuid.uuid4()))

    translations = TranslatedFields(
        subject=models.CharField(max_length=100,),
        content=models.TextField()
    )


class FaqCategory(TranslatableModel):
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=20)

    translations = TranslatedFields(
        name=models.CharField(max_length=200, null=True),
    )

    class Meta:
        verbose_name = _('FAQ Category')
        verbose_name_plural = _('FAQ Categories')

    def __unicode__(self):
        return '%s' % self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('support-faq-by-category', [self.slug])


class Faq(TranslatableModel):
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True)
    is_active = models.BooleanField()
    view_count = models.IntegerField(null=True)
    related_questions = models.ManyToManyField('self', null=True, blank=True)
    category = models.ForeignKey(FaqCategory, null=True, blank=True)

    translations = TranslatedFields(
        question=models.CharField(max_length=200, null=True),
        answer=models.TextField(null=True)
    )

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('support-view-faq', [self.category.slug, self.slug])

    def save(self, *args, **kwargs):
        if not self.id:
            # populate published_at
            self.published_at = datetime.utcnow().replace(tzinfo=utc)
        super(Faq, self).save(*args, **kwargs)
