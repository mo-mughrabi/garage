# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from django.utils.translation import ugettext_lazy as _


class Product(TranslatableModel):
    price = models.DecimalField(_('Price'), max_digits=12, decimal_places=3, default=0)

    translations        = TranslatedFields(
        name        = models.CharField(max_length=100,),
        description = models.TextField(null=True, blank=True)
    )


class Order(models.Model):
    product         = models.ForeignKey(Product)
    user            = models.ForeignKey(User)