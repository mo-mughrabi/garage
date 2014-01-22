# -*- coding: utf-8 -*-
from models import Faq, FaqCategory, Content
from django.contrib import admin
from hvad.admin import TranslatableAdmin, TranslatableTabularInline


class FaqCategoryForm(TranslatableAdmin):
    pass


class FaqForm(TranslatableAdmin):
    list_display = ('__unicode__', )
    exclude = ('created_at', 'view_count', 'published_at', )


admin.site.register(Faq, FaqForm)
admin.site.register(FaqCategory, FaqCategoryForm)
